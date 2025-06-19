import os
import sys
import argparse # Added for command line argument parsing
import json
import gzip
import shutil
from PIL import Image
from typing import Tuple, List, Union # For potential future type hinting
from io import BytesIO
import base64

# === Configuration ===

ICON_SPECS = [
    (16, "favicon-16x16.png", "PNG"),
    (32, "favicon-32x32.png", "PNG"),
    (48, "favicon-48x48.png", "PNG"),
    (57, "apple-touch-icon-57x57.png", "PNG"),
    (57, "apple-touch-icon-57x57-precomposed.png", "PNG"),
    (72, "apple-touch-icon-72x72.png", "PNG"),
    (76, "apple-touch-icon-76x76.png", "PNG"),
    (114, "apple-touch-icon-114x114.png", "PNG"),
    (120, "apple-touch-icon-120x120.png", "PNG"),
    (128, "favicon-128x128.png", "PNG"),
    (144, "android-chrome-144x144.png", "PNG"),
    (152, "apple-touch-icon-152x152.png", "PNG"),
    (152, "apple-touch-icon.png", "PNG"),
    (152, "apple-touch-icon-precomposed.png", "PNG"),
    (167, "apple-touch-icon-167x167.png", "PNG"),
    (180, "apple-touch-icon-180x180.png", "PNG"),
    (192, "android-chrome-192x192.png", "PNG"),
    (256, "favicon-256x256.png", "PNG"),
    (512, "android-chrome-512x512.png", "PNG"),
    (70, "mstile-70x70.png", "PNG"),
    (150, "mstile-150x150.png", "PNG"),
    (310, "mstile-310x310.png", "PNG"),
    ((310, 150), "mstile-310x150.png", "PNG"),
]

ICO_SIZES = [16, 32, 48, 64, 128, 256]
# OUTPUT_DIR is now dynamically generated in generate_icons
# Default base name for output directory if needed outside generate_icons context
DEFAULT_OUTPUT_DIR_BASE = "favicons"


from PIL import Image as PilImageModule # Added for type hint clarity

def ensure_square_aspect_by_padding(image: PilImageModule.Image) -> PilImageModule.Image:
    """Makes an image square by adding transparent padding, maintaining original content."""
    # Convert to RGBA to handle transparency consistently and allow transparent padding
    img_rgba = image.convert("RGBA")
    width, height = img_rgba.size

    if width == height:
        return img_rgba  # Already square, and in RGBA mode

    max_side = max(width, height)
    
    # Create a new square canvas with a transparent background
    square_canvas = PilImageModule.new("RGBA", (max_side, max_side), (0, 0, 0, 0))
    
    # Calculate position to paste the original image onto the center of the canvas
    paste_x = (max_side - width) // 2
    paste_y = (max_side - height) // 2
    
    # Paste the original image (as RGBA) onto the transparent canvas
    # Using img_rgba as its own mask ensures alpha channel is respected
    square_canvas.paste(img_rgba, (paste_x, paste_y), img_rgba)
    
    return square_canvas


def pad_and_resize(image, target_size):
    """
    Resizes an image to fit within the target_size dimensions, adding transparent padding.
    Maintains the original aspect ratio of the content.
    """
    if isinstance(target_size, int):
        if target_size <= 0:
            # Handle degenerate case: if target is 0 or negative, what should happen?
            # For now, let's assume it implies a 1x1 or smallest possible, or raise error.
            # Raising an error is safer for now.
            raise ValueError("Target dimension must be positive.")
        target_w, target_h = target_size, target_size
    else:
        target_w, target_h = target_size
        if target_w <= 0 or target_h <= 0:
            raise ValueError("Target dimensions must be positive.")

    original_w, original_h = image.size

    if original_w <= 0 or original_h <= 0:
        # If original image is degenerate, return an empty transparent image of target size
        return Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

    # Calculate the scaling factor to fit the image within the target dimensions
    scale = min(target_w / original_w, target_h / original_h)
    
    # Calculate new dimensions for the scaled image
    new_w = int(original_w * scale)
    new_h = int(original_h * scale)

    # Ensure new dimensions are at least 1x1 for resize, if target allows
    if new_w == 0 and target_w > 0: new_w = 1
    if new_h == 0 and target_h > 0: new_h = 1
    
    # If scaled dimensions are zero (e.g. original was 1xN and target is Nx0),
    # it's impossible to resize meaningfully. Return transparent target.
    if new_w <= 0 or new_h <= 0:
        return Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

    # Resize the image using LANCZOS for high quality
    scaled_image = image.resize((new_w, new_h), Image.LANCZOS)

    # If the scaled image is in Palette mode ('P') and might have transparency,
    # convert to 'RGBA' to ensure the alpha channel is handled correctly during paste.
    if scaled_image.mode == 'P' and 'transparency' in scaled_image.info:
        scaled_image = scaled_image.convert('RGBA')
    elif scaled_image.mode == 'LA' or scaled_image.mode == 'PA': # LA is L with Alpha, PA is P with Alpha
        scaled_image = scaled_image.convert('RGBA') # Ensure full RGBA for consistent pasting
    
    # Create a new image with a transparent background (RGBA)
    padded_image = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    
    # Calculate coordinates to paste the scaled image onto the center of the padded image
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2

    # Paste the scaled image. If scaled_image has an alpha channel (e.g., RGBA or LA),
    # it will be used for blending. Otherwise, it's an opaque paste.
    if scaled_image.mode in ['RGBA', 'LA']:
        padded_image.paste(scaled_image, (paste_x, paste_y), mask=scaled_image)
    else:
        padded_image.paste(scaled_image, (paste_x, paste_y))
    
    return padded_image


def save_png(img, size, filename, output_dir):
    resized_and_padded = pad_and_resize(img, size)
    path = os.path.join(output_dir, filename)
    resized_and_padded.save(path, format="PNG", optimize=True)


def save_ico(img, sizes, output_dir, filename="favicon.ico"):
    # For ICO, target_size for pad_and_resize should be an int (square)
    processed_icons = [pad_and_resize(img, sz) for sz in sizes]
    path = os.path.join(output_dir, filename)
    
    # Ensure all images are in a mode supported by ICO (e.g., RGBA)
    # pad_and_resize already returns RGBA, so this conversion might be redundant
    # but kept for safety if pad_and_resize changes.
    final_icons = []
    for icon_img in processed_icons:
        if icon_img.mode != 'RGBA':
            final_icons.append(icon_img.convert('RGBA'))
        else:
            final_icons.append(icon_img)
    
    if final_icons:
        # The `sizes` argument in save() for ICO is more of a hint or for specific source formats.
        # Pillow typically derives sizes from the provided image objects themselves.
        # Providing append_images is the correct way to make a multi-resolution ICO.
        final_icons[0].save(path, format="ICO", append_images=final_icons[1:])
    else:
        print(f"Warning: No icons generated for {filename}")


def save_svg_with_png(img, output_dir, filename="safari-pinned-tab.svg"):
    svg_template = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><image href="data:image/png;base64,{data}" height="512" width="512"/></svg>'
    # For SVG pinned tab, it's usually a square 512x512 image.
    resized_and_padded = pad_and_resize(img, 512) # pad_and_resize with int for square
    buffer = BytesIO()
    # Ensure the image saved into the buffer is RGBA for transparency in SVG
    if resized_and_padded.mode != 'RGBA':
        resized_and_padded = resized_and_padded.convert('RGBA')
    resized_and_padded.save(buffer, format="PNG", optimize=True)
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    svg_data = svg_template.format(data=b64_data)
    with open(os.path.join(output_dir, filename), "w") as f:
        f.write(svg_data)


def save_manifest(output_dir):
    # Construct paths relative to the dynamic output directory
    # The 'src' paths in the manifest should be absolute from the web server root,
    # so they should reflect the output_dir name.
    manifest = {
        "name": "Web App",
        "icons": [
            {
                "src": f"/{output_dir}/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": f"/{output_dir}/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"
    }
    with open(os.path.join(output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, separators=(',', ':'))


def gzip_all_files(output_dir):
    for fname in os.listdir(output_dir):
        path = os.path.join(output_dir, fname)
        if os.path.isfile(path) and not fname.lower().endswith(".png"):
            gz_path = path + ".gz"
            with open(path, "rb") as f_in:
                with gzip.open(gz_path, "wb", compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)


def generate_icons(source_image_path, crop_enabled=True, high_quality=False):
    if not os.path.isfile(source_image_path):
        raise FileNotFoundError(f"Error: File '{source_image_path}' not found.")

    # Generate dynamic output directory name
    source_basename = os.path.splitext(os.path.basename(source_image_path))[0]
    output_dir = f"favicons-{source_basename}"
    
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(source_image_path) # Keep original mode initially
    # Convert to RGBA before any processing that might need it (like padding or quantization)
    # This ensures consistent handling, especially if the source is paletted with transparency.
    img = img.convert("RGBA")

    if crop_enabled: # If True (default), image is made square by padding. If False (--no-crop), original aspect is kept.
        img = ensure_square_aspect_by_padding(img)

    # Attempt to quantize the image to 256 colors (8-bit palette) to reduce PNG sizes.
    # This converts the image to 'P' mode. Pillow's quantize handles RGBA source
    # and attempts to preserve transparency by dedicating a palette entry if needed.
    # Dither.NONE (or 0) is used to avoid patterns that might increase file size.
    quantized_method_used = None
    if not high_quality:
        print("Note: Standard quality mode. Attempting image quantization to 256 colors.")
        try:
            dither_setting = getattr(Image.Dither, "NONE", 0) # Use enum if available, else 0 for no dither

            # Attempt 1: LIBIMAGEQUANT (high quality for 256 colors)
            try:
                libimagequant_enum_val = Image.Quantize.LIBIMAGEQUANT
                print("Note: Attempting image quantization using LIBIMAGEQUANT with up to 256 colors...")
                img_quantized = img.quantize(colors=256, method=libimagequant_enum_val, dither=dither_setting)
                img = img_quantized
                quantized_method_used = "LIBIMAGEQUANT"
                print("Note: Image quantization successful with LIBIMAGEQUANT (target 256 colors).")
            except AttributeError:
                print("Warning: Pillow's LIBIMAGEQUANT quantization method not found. Trying FASTOCTREE fallback.")
            except OSError as e_os:
                print(f"Warning: LIBIMAGEQUANT quantization failed (OSError: {e_os}). Trying FASTOCTREE fallback.")
            except ValueError as e_val:
                print(f"Warning: LIBIMAGEQUANT quantization failed (ValueError: {e_val}). Trying FASTOCTREE fallback.")
            
            # Attempt 2: FASTOCTREE (fallback, if LIBIMAGEQUANT was not successful)
            if not quantized_method_used:
                try:
                    fastoctree_enum_val = Image.Quantize.FASTOCTREE
                    print("Note: Attempting image quantization using FASTOCTREE with up to 256 colors...")
                    img_quantized = img.quantize(colors=256, method=fastoctree_enum_val, dither=dither_setting)
                    img = img_quantized
                    quantized_method_used = "FASTOCTREE"
                    print("Note: Image quantization successful with FASTOCTREE (target 256 colors).")
                except AttributeError:
                     print("Warning: Pillow's FASTOCTREE quantization method not found. This is unexpected. Proceeding with original colors.")
                except ValueError as e_fastoctree_val:
                    print(f"Warning: FASTOCTREE quantization failed (ValueError: {e_fastoctree_val}). Proceeding with original colors.")
                except Exception as e_fastoctree:
                    print(f"Warning: FASTOCTREE quantization also failed ({type(e_fastoctree).__name__}: {e_fastoctree}). Proceeding with original colors.")

        except Exception as e_quantize_setup:
            print(f"Warning: An error occurred during quantization setup ({type(e_quantize_setup).__name__}: {e_quantize_setup}). Proceeding with original colors.")

        if not quantized_method_used:
            print("Note: Proceeding with original image colors as quantization was not successful.")
    else:
        print("Note: High quality mode enabled. Skipping quantization, using original RGBA image.")

    # 'img' is now either quantized ('P' mode) or original ('RGBA' mode if quantization failed)

    for size, filename, fmt in ICON_SPECS:
        save_png(img, size, filename, output_dir)

    save_ico(img, ICO_SIZES, output_dir)
    save_svg_with_png(img, output_dir)
    save_manifest(output_dir)
    gzip_all_files(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate favicons from a source image.")
    parser.add_argument("source_image", help="Path to the source image file (e.g., your_image.png)")
    parser.add_argument("--no-crop", action="store_false", dest="crop_enabled", default=True,
                        help="Disable automatic square padding/cropping. Icons will maintain original aspect ratio within target dimensions.")
    parser.add_argument("--highquality", action="store_true", default=False,
                        help="Save PNGs as full RGBA without color quantization. Results in larger files but preserves all colors.")

    args = parser.parse_args()

    try:
        # Determine output directory name for the print message
        source_basename = os.path.splitext(os.path.basename(args.source_image))[0]
        dynamic_output_dir = f"favicons-{source_basename}"
        generate_icons(args.source_image, crop_enabled=args.crop_enabled, high_quality=args.highquality)
        print(f"✅ Icons generated successfully in the '{dynamic_output_dir}/' folder.")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating icons: {e}")
        sys.exit(1)
