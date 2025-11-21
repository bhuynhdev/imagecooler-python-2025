#!/usr/bin/env python3
"""
Resize each image in a source folder to prepare as source material for photomosaics effect.
"""

import os
import argparse
from PIL import Image, ImageOps

def _build_default_output_path(source_path):
    """
    If source_path contains a 'source_images' directory:
        Return:
        <project_root>/photomosaics/processed_source_images/<remainder_after_source_images>

    Else:
        Return as a sibling directory:
        <parent>/<input_folder_name>_processed
    """
    abs_path = os.path.abspath(source_path)
    parts = abs_path.split(os.sep)

    if "source_images" in parts:
        idx = parts.index("source_images")
        project_root = os.sep.join(parts[:idx])
        remainder = os.sep.join(parts[idx + 1 :])
        return os.path.join(
            project_root,
            "processed_source_images",
            f"{remainder}_processed"
        )
    else:
        parent = os.path.dirname(abs_path)
        base_name = os.path.basename(abs_path)
        return os.path.join(parent, f"{base_name}_processed")


def process_source_images(source_folder_path: str, square_size: int, output_folder_path: str):
    """
    Resize each image in source_path to square_size x square_size
    and save into output_path as WebP with default quality=75.
    """

    if not os.path.isdir(source_folder_path):
        raise ValueError(f"Source folder not found: {source_folder_path}")

    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(source_folder_path):
        input_img_path = os.path.join(source_folder_path, filename)

        if not os.path.isfile(input_img_path):
            continue

        try:
            with Image.open(input_img_path) as img:
                # Resize using ImageOps.fit
                processed_img = ImageOps.fit(img, (square_size, square_size))
                # Build output path with .webp extension
                base_name, _ = os.path.splitext(filename)
                out_path = os.path.join(output_folder_path, f"{base_name}.webp")
                # Save as WebP with default quality 75
                processed_img.save(out_path, format="WEBP", quality=75)
                print(f"Processed: {filename} -> {out_path}")
        except Exception as e:
            print(f"Skipping {filename}: {e}")

    print(f"Done. Output in: {output_folder_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images in a folder to square thumbnails for photomosaics.")

    parser.add_argument("input_folder", help="Folder containing the original source images.")

    # Optional positional output folder
    parser.add_argument("output_folder", nargs="?", help="Optional output folder. If omitted, a default path is generated.")

    parser.add_argument(
        "--square-size",
        type=int,
        default=35,
        help="Size (in pixels) for both width and height (default: 35)."
    )

    args = parser.parse_args()

    output_folder = args.output_folder or _build_default_output_path(args.input_folder)

    process_source_images(
        args.input_folder,
        args.square_size,
        output_folder
    )
