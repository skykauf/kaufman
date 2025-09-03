#!/usr/bin/env python3
"""
Simple server to serve recipe images for the pair viewer
"""

import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from PIL import Image
import pillow_heif
import io
import base64


class RecipeImageHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Get the absolute path to the mimi_recipe_pictures directory
        self.images_dir = Path(__file__).parent.parent.parent / "mimi_recipe_pictures"
        print(f"Images directory: {self.images_dir}")
        print(f"Directory exists: {self.images_dir.exists()}")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/images":
            self.send_image_list()
        elif path.startswith("/api/image/"):
            self.send_image(path[11:])  # Remove '/api/image/' prefix
        elif path == "/":
            # Serve the HTML viewer
            self.path = "/recipe_pair_viewer.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def send_image_list(self):
        """Send list of all image files"""
        try:
            image_extensions = {".jpg", ".jpeg", ".png", ".heic", ".bmp", ".tiff"}
            image_files = [
                f.name
                for f in self.images_dir.iterdir()
                if f.is_file() and f.suffix.lower() in image_extensions
            ]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(image_files).encode("utf-8"))

        except Exception as e:
            self.send_error(500, f"Error reading image list: {str(e)}")

    def send_image(self, filename):
        """Send a specific image file, converting HEIC to JPEG if needed"""
        try:
            # Decode the filename
            filename = urllib.parse.unquote(filename)
            image_path = self.images_dir / filename
            print(f"Requested filename: {filename}")
            print(f"Full image path: {image_path}")
            print(f"Image exists: {image_path.exists()}")

            if not image_path.exists():
                self.send_error(404, f"Image not found: {filename}")
                return

            # Check if it's a HEIC file
            if image_path.suffix.lower() == ".heic":
                # Convert HEIC to JPEG
                try:
                    heif_file = pillow_heif.read_heif(image_path)
                    if heif_file.data is not None:
                        image = Image.frombytes(
                            heif_file.mode,
                            heif_file.size,
                            heif_file.data,
                            "raw",
                            heif_file.mode,
                            heif_file.stride,
                        )
                    else:
                        raise Exception("Failed to read HEIC data")

                    # Convert to RGB if necessary
                    if image.mode != "RGB":
                        image = image.convert("RGB")

                    # Save as JPEG to memory
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG", quality=95)
                    buffer.seek(0)

                    self.send_response(200)
                    self.send_header("Content-type", "image/jpeg")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()

                    self.wfile.write(buffer.getvalue())
                    return

                except Exception as heif_error:
                    print(f"HEIC conversion failed for {filename}: {heif_error}")
                    # Fall back to trying to serve as regular image
                    pass

            # For non-HEIC files or if HEIC conversion failed, serve as-is
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            with open(image_path, "rb") as f:
                self.wfile.write(f.read())

        except Exception as e:
            self.send_error(500, f"Error serving image {filename}: {str(e)}")


def main():
    port = 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, RecipeImageHandler)

    print(f"Starting recipe image server on port {port}")
    print(f"Open http://localhost:{port} to view recipe pairs")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    main()
