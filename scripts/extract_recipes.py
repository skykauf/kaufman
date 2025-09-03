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

def extract_recipe_from_image_pair(image_paths: List[Path]) -> Dict[str, Any]:
    """Extract recipe data from a pair of images (front and back) using OpenAI Vision API."""
    image_names = [path.name for path in image_paths]
    print(f"Processing recipe pair: {image_names[0]} (front) + {image_names[1]} (back)")
    
    # Encode both images
    base64_images = []
    failed_images = []
    for image_path in image_paths:
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            failed_images.append(image_path.name)
        else:
            base64_images.append(base64_image)
    
    # If either image failed, mark the entire recipe pair as lost
    if failed_images:
        error_msg = f"Recipe pair lost - failed to process images: {', '.join(failed_images)}"
        print(f"❌ {error_msg}")
        return {
            "error": error_msg,
            "recipe_lost": True,
            "failed_images": failed_images,
            "source_images": image_names,
            "front_image": image_names[0],
            "back_image": image_names[1]
        }
    
    try:
        # Prepare content with both images
        content_items = [
            {
                "type": "text",
                "text": "Please extract the complete recipe information from these two images. The first image is the FRONT of the recipe card, and the second image is the BACK of the recipe card. Combine information from both sides to provide comprehensive recipe data in the specified JSON format."
            }
        ]
        
        # Add both images
        for base64_image in base64_images:
            content_items.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": content_items
                }
            ],
            max_tokens=1500,  # Increased for more comprehensive responses
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
            recipe_data["source_images"] = image_names
            recipe_data["front_image"] = image_names[0]
            recipe_data["back_image"] = image_names[1]
            return recipe_data
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from response for recipe pair {image_names}: {e}")
            return {
                "error": "Failed to parse JSON response",
                "raw_response": content,
                "source_images": image_names
            }
    
    except Exception as e:
        print(f"Error calling OpenAI API for recipe pair {image_names}: {e}")
        return {"error": str(e), "source_images": image_names}

def extract_recipe_from_single_image(image_path: Path) -> Dict[str, Any]:
    """Extract recipe data from a single image (for backward compatibility)."""
    print(f"Processing single image: {image_path.name}")
    
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
    """Process all photos in the mimi_recipe_pictures directory as recipe pairs."""
    pictures_dir = Path(__file__).parent.parent / "mimi_recipe_pictures"
    
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
    
    # Sort files to ensure correct pairing
    image_files = sorted(image_files)
    
    print(f"Found {len(image_files)} image files to process...")
    print("\nFile format analysis:")
    for img_file in image_files:
        format_info = get_file_format_info(img_file)
        print(f"  {img_file.name}: {format_info}")
    print()
    
    # Check if we have an even number of images for pairing
    if len(image_files) % 2 != 0:
        print(f"⚠️  Warning: Odd number of images ({len(image_files)}). Last image will be processed alone.")
    
    # Process images in pairs
    results = []
    for i in range(0, len(image_files), 2):
        if i + 1 < len(image_files):
            # Process as a pair (front + back)
            image_pair = [image_files[i], image_files[i + 1]]
            result = extract_recipe_from_image_pair(image_pair)
            results.append(result)
            
            if "recipe_lost" in result and result["recipe_lost"]:
                print(f"⚠️  Recipe pair lost: {image_files[i].name} + {image_files[i + 1].name}")
            else:
                print(f"✅ Completed recipe pair: {image_files[i].name} + {image_files[i + 1].name}")
        else:
            # Process single image if odd number
            print(f"Processing single image: {image_files[i].name}")
            result = extract_recipe_from_single_image(image_files[i])
            results.append(result)
            print(f"Completed single image: {image_files[i].name}")
        
        print("-" * 50)
    
    return results

def save_results(results: List[Dict[str, Any]], output_file: str = "extracted_recipes.json"):
    """Save the extracted recipe data to a JSON file."""
    # Ensure the output file is saved in the kaufman directory
    output_path = Path(__file__).parent.parent / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {output_path}")

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
            recipe_pairs_lost = sum(1 for r in results if "recipe_lost" in r and r["recipe_lost"])
            
            print("\n" + "=" * 60)
            print(f"Processing complete!")
            print(f"Successfully processed: {successful} recipes")
            print(f"Failed: {failed} recipes")
            if recipe_pairs_lost > 0:
                print(f"Recipe pairs lost: {recipe_pairs_lost}")
            print(f"Total processed: {len(results)} recipes")
            
            if failed > 0:
                print("\nFailed recipes:")
                for result in results:
                    if "error" in result:
                        if "recipe_lost" in result and result["recipe_lost"]:
                            print(f"  - Recipe pair lost: {result.get('front_image', 'Unknown')} + {result.get('back_image', 'Unknown')}")
                            print(f"    Reason: {result['error']}")
                        else:
                            print(f"  - {result.get('source_image', 'Unknown')}: {result['error']}")
        
        else:
            print("No results to save.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

def test_single_image(image_name: str):
    """Test processing of a single image for debugging."""
    pictures_dir = Path(__file__).parent.parent / "mimi_recipe_pictures"
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

def test_image_pair(image1_name: str, image2_name: str):
    """Test processing of an image pair for debugging."""
    pictures_dir = Path(__file__).parent.parent / "mimi_recipe_pictures"
    image1_path = pictures_dir / image1_name
    image2_path = pictures_dir / image2_name
    
    if not image1_path.exists():
        print(f"Image {image1_name} not found!")
        return
    if not image2_path.exists():
        print(f"Image {image2_name} not found!")
        return
    
    print(f"Testing image pair: {image1_name} (front) + {image2_name} (back)")
    print("=" * 50)
    
    # Show file format info for both
    for img_path, role in [(image1_path, "Front"), (image2_path, "Back")]:
        format_info = get_file_format_info(img_path)
        print(f"{role} image ({img_path.name}): {format_info}")
    print()
    
    # Try to encode both images
    print("Attempting to encode both images...")
    base64_data1 = encode_image_to_base64(image1_path)
    base64_data2 = encode_image_to_base64(image2_path)
    
    if base64_data1 and base64_data2:
        print(f"✅ Successfully encoded both images!")
        print(f"Front image base64 length: {len(base64_data1)} characters")
        print(f"Back image base64 length: {len(base64_data2)} characters")
        total_size = (len(base64_data1) + len(base64_data2)) * 3 // 4 / 1024
        print(f"Total estimated size: {total_size:.1f} KB")
    else:
        print("❌ Failed to encode one or both images")
    
    print("=" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        if len(sys.argv) == 3:
            test_single_image(sys.argv[2])
        elif len(sys.argv) == 4:
            test_image_pair(sys.argv[2], sys.argv[3])
        else:
            print("Usage:")
            print("  Single image: python extract_recipes.py --test <image_name>")
            print("  Image pair:   python extract_recipes.py --test <front_image> <back_image>")
            print("Examples:")
            print("  python extract_recipes.py --test IMG_6165.HEIC")
            print("  python extract_recipes.py --test IMG_6165.HEIC IMG_6166.HEIC")
    else:
        main()
