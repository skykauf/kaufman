#!/usr/bin/env python3
"""
Recipe Photo Processor

This script processes all photos in the mimi_recipe_pictures directory and submits them
to OpenAI's Vision API to extract recipe data in structured JSON format.
"""

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Any
import openai
from PIL import Image
import pillow_heif

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# System prompt for recipe extraction
SYSTEM_PROMPT = """You are a recipe extraction expert. Analyze the provided image and extract recipe information in the following structured JSON format:

{
  "recipe_name": "Name of the recipe",
  "ingredients": [
    {
      "item": "ingredient name",
      "amount": "quantity and unit",
      "notes": "any additional notes or preparation instructions"
    }
  ],
  "instructions": [
    "Step 1: First instruction",
    "Step 2: Second instruction"
  ],
  "cooking_time": "estimated cooking time",
  "servings": "number of servings",
  "difficulty": "easy/medium/hard",
  "cuisine_type": "type of cuisine if identifiable",
  "dietary_info": ["vegetarian", "gluten-free", etc. if applicable],
  "notes": "any additional notes or observations"
}

Be as detailed and accurate as possible. If any information is unclear or not visible, use "unknown" or "not specified" as appropriate."""

def encode_image_to_base64(image_path: Path) -> str:
    """Convert image to base64 string for OpenAI API."""
    try:
        # Try to detect the actual file format by reading the first few bytes
        with open(image_path, 'rb') as f:
            header = f.read(12)
        
        # Check if it's actually a HEIC file
        is_heic = (image_path.suffix.lower() == '.heic' and 
                   (b'ftyp' in header or b'heic' in header or b'heix' in header))
        
        if is_heic:
            try:
                heif_file = pillow_heif.read_heif(image_path)
                image = Image.frombytes(
                    heif_file.mode, 
                    heif_file.size, 
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
            except Exception as heif_error:
                print(f"HEIC processing failed for {image_path.name}, trying as regular image: {heif_error}")
                # Fall back to regular image processing
                image = Image.open(image_path)
        else:
            # Try to open as regular image
            image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPEG in memory and encode
        import io
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        # Try alternative approach - use system tools if available
        try:
            return _try_alternative_image_processing(image_path)
        except Exception as alt_error:
            print(f"Alternative processing also failed for {image_path.name}: {alt_error}")
            return None

def _try_alternative_image_processing(image_path: Path) -> str:
    """Try alternative methods to process problematic images."""
    import subprocess
    import tempfile
    
    # Try using sips (macOS) to convert HEIC to JPEG
    try:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # Use sips to convert HEIC to JPEG
        result = subprocess.run([
            'sips', '-s', 'format', 'jpeg', 
            str(image_path), '--out', tmp_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(tmp_path):
            # Read the converted image
            with open(tmp_path, 'rb') as f:
                image_data = f.read()
            os.unlink(tmp_path)  # Clean up temp file
            return base64.b64encode(image_data).decode('utf-8')
        else:
            raise Exception(f"sips conversion failed: {result.stderr}")
            
    except Exception as e:
        # Clean up temp file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e

def extract_recipe_from_image(image_path: Path) -> Dict[str, Any]:
    """Extract recipe data from a single image using OpenAI Vision API."""
    print(f"Processing: {image_path.name}")
    
    # Encode image
    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return {"error": f"Failed to process image {image_path.name}"}
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract the recipe information from this image and provide it in the specified JSON format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Try to parse JSON from the response
        try:
            # Look for JSON content in the response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            else:
                json_content = content.strip()
            
            recipe_data = json.loads(json_content)
            recipe_data["source_image"] = image_path.name
            return recipe_data
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from response for {image_path.name}: {e}")
            return {
                "error": "Failed to parse JSON response",
                "raw_response": content,
                "source_image": image_path.name
            }
    
    except Exception as e:
        print(f"Error calling OpenAI API for {image_path.name}: {e}")
        return {"error": str(e), "source_image": image_path.name}

def get_file_format_info(file_path: Path) -> str:
    """Get information about the actual file format by examining the file header."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
        
        # Common file signatures
        signatures = {
            b'\xff\xd8\xff': 'JPEG',
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'GIF87a': 'GIF',
            b'GIF89a': 'GIF',
            b'BM': 'BMP',
            b'II*\x00': 'TIFF (little-endian)',
            b'MM\x00*': 'TIFF (big-endian)',
            b'ftyp': 'HEIC/MP4',
            b'heic': 'HEIC',
            b'heix': 'HEIC'
        }
        
        detected_format = 'Unknown'
        for signature, format_name in signatures.items():
            if header.startswith(signature) or signature in header:
                detected_format = format_name
                break
        
        return f"Extension: {file_path.suffix}, Detected: {detected_format}, Size: {file_path.stat().st_size / (1024*1024):.1f}MB"
    
    except Exception as e:
        return f"Error reading file header: {e}"

def process_all_recipe_photos() -> List[Dict[str, Any]]:
    """Process all photos in the mimi_recipe_pictures directory."""
    pictures_dir = Path("mimi_recipe_pictures")
    
    if not pictures_dir.exists():
        print(f"Directory {pictures_dir} not found!")
        return []
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.bmp', '.tiff'}
    image_files = [
        f for f in pictures_dir.iterdir() 
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        print("No image files found in the directory!")
        return []
    
    print(f"Found {len(image_files)} image files to process...")
    print("\nFile format analysis:")
    for img_file in sorted(image_files):
        format_info = get_file_format_info(img_file)
        print(f"  {img_file.name}: {format_info}")
    print()
    
    # Process each image
    results = []
    for image_file in sorted(image_files):
        result = extract_recipe_from_image(image_file)
        results.append(result)
        print(f"Completed: {image_file.name}")
        print("-" * 50)
    
    return results

def save_results(results: List[Dict[str, Any]], output_file: str = "extracted_recipes.json"):
    """Save the extracted recipe data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {output_file}")

def main():
    """Main function to run the recipe extraction process."""
    print("Starting recipe photo processing...")
    print("=" * 60)
    
    try:
        # Process all photos
        results = process_all_recipe_photos()
        
        if results:
            # Save results
            save_results(results)
            
            # Print summary
            successful = sum(1 for r in results if "error" not in r)
            failed = len(results) - successful
            
            print("\n" + "=" * 60)
            print(f"Processing complete!")
            print(f"Successfully processed: {successful} images")
            print(f"Failed: {failed} images")
            print(f"Total processed: {len(results)} images")
            
            if failed > 0:
                print("\nFailed images:")
                for result in results:
                    if "error" in result:
                        print(f"  - {result.get('source_image', 'Unknown')}: {result['error']}")
        
        else:
            print("No results to save.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

def test_single_image(image_name: str):
    """Test processing of a single image for debugging."""
    pictures_dir = Path("mimi_recipe_pictures")
    image_path = pictures_dir / image_name
    
    if not image_path.exists():
        print(f"Image {image_name} not found!")
        return
    
    print(f"Testing single image: {image_name}")
    print("=" * 50)
    
    # Show file format info
    format_info = get_file_format_info(image_path)
    print(f"File info: {format_info}")
    print()
    
    # Try to encode the image
    print("Attempting to encode image...")
    base64_data = encode_image_to_base64(image_path)
    
    if base64_data:
        print(f"✅ Successfully encoded image!")
        print(f"Base64 length: {len(base64_data)} characters")
        print(f"Estimated size: {len(base64_data) * 3 // 4 / 1024:.1f} KB")
    else:
        print("❌ Failed to encode image")
    
    print("=" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        if len(sys.argv) > 2:
            test_single_image(sys.argv[2])
        else:
            print("Usage: python extract_recipes.py --test <image_name>")
            print("Example: python extract_recipes.py --test IMG_6165.HEIC")
    else:
        main()
