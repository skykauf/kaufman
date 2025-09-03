#!/usr/bin/env python3
"""
Quick script to check recipe card pairs
"""

import os
from pathlib import Path
import subprocess
import sys


def list_recipe_pairs():
    """List all recipe pairs in the mimi_recipe_pictures directory"""
    pictures_dir = Path(__file__).parent.parent / "mimi_recipe_pictures"

    if not pictures_dir.exists():
        print(f"Directory {pictures_dir} not found!")
        return

    # Get all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".heic", ".bmp", ".tiff"}
    image_files = [
        f
        for f in pictures_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print("No image files found!")
        return

    # Sort files to ensure proper pairing
    image_files = sorted(image_files)

    print(f"Found {len(image_files)} image files")
    print("=" * 60)

    # Group into pairs
    pairs = []
    for i in range(0, len(image_files), 2):
        if i + 1 < len(image_files):
            pairs.append((image_files[i], image_files[i + 1]))
        else:
            pairs.append((image_files[i], None))

    print(f"Recipe pairs ({len(pairs)} total):")
    print()

    for i, (front, back) in enumerate(pairs):
        print(f"Pair {i+1}:")
        print(f"  Front: {front.name}")
        if back:
            print(f"  Back:  {back.name}")
        else:
            print(f"  Back:  (no back image)")
        print()


def open_image_pair(pair_index):
    """Open a specific image pair using the default system viewer"""
    pictures_dir = Path(__file__).parent.parent / "mimi_recipe_pictures"

    # Get all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".heic", ".bmp", ".tiff"}
    image_files = [
        f
        for f in pictures_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print("No image files found!")
        return

    # Sort files
    image_files = sorted(image_files)

    # Calculate pair index
    pair_start = (pair_index - 1) * 2
    if pair_start >= len(image_files):
        print(f"Pair {pair_index} not found!")
        return

    front = image_files[pair_start]
    back = image_files[pair_start + 1] if pair_start + 1 < len(image_files) else None

    print(f"Opening pair {pair_index}:")
    print(f"  Front: {front.name}")
    if back:
        print(f"  Back:  {back.name}")
    else:
        print(f"  Back:  (no back image)")
    print()

    # Open images with system default viewer
    try:
        subprocess.run(["open", str(front)])
        if back:
            subprocess.run(["open", str(back)])
        print("Images opened in default viewer")
    except Exception as e:
        print(f"Error opening images: {e}")


def main():
    if len(sys.argv) == 1:
        # Just list all pairs
        list_recipe_pairs()
    elif len(sys.argv) == 2 and sys.argv[1] == "--list":
        list_recipe_pairs()
    elif len(sys.argv) == 3 and sys.argv[1] == "--open":
        try:
            pair_index = int(sys.argv[2])
            open_image_pair(pair_index)
        except ValueError:
            print("Please provide a valid pair number")
    else:
        print("Usage:")
        print("  python check_recipe_pairs.py                    # List all pairs")
        print("  python check_recipe_pairs.py --list            # List all pairs")
        print("  python check_recipe_pairs.py --open <number>   # Open specific pair")
        print()
        print("Examples:")
        print("  python check_recipe_pairs.py")
        print("  python check_recipe_pairs.py --open 5")


if __name__ == "__main__":
    main()
