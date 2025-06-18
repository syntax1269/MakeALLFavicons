import os
import sys
import json
import gzip
import shutil
from PIL import Image
from io import BytesIO
import base64

# === Configuration ===

ICON_SPECS = [
    (16, "favicon-16x16.png", "PNG"),
    (32, "favicon-32x32.png", "PNG"),
    (48, "favicon-48x48.png", "PNG"),
    (72, "apple-touch-icon-72x72.png", "PNG"),
    (76, "apple-touch-icon-76x76.png", "PNG"),
    (114, "apple-touch-icon-114x114.png", "PNG"),
    (120, "apple-touch-icon-120x120.png", "PNG"),
    (128, "favicon-128x128.png", "PNG"),
    (144, "android-chrome-144x144.png", "PNG"),
    (152, "apple-touch-icon-152x152.png", "PNG"),
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
OUTPUT_DIR = "favicons"


def crop_to_square(image):
    width, height = image.size
    if width == height:
        return image
    min_side = min(width, height)
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    return image.crop((left, top, left + min_side, top + min_side))


def resize_image(img, size):
    if isinstance(size, tuple):
        return img.resize(size, Image.LANCZOS)
    return img.resize((size, size), Image.LANCZOS)


def save_png(img, size, filename):
    resized = resize_image(img, size)
    path = os.path.join(OUTPUT_DIR, filename)
    resized.save(path, format="PNG")


def save_ico(img, sizes, filename="favicon.ico"):
    icons = [resize_image(img, (sz, sz)) for sz in sizes]
    path = os.path.join(OUTPUT_DIR, filename)
    icons[0].save(path, format="ICO", sizes=[(sz, sz) for sz in sizes])


def save_svg_with_png(img, filename="safari-pinned-tab.svg"):
    svg_template = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <image href="data:image/png;base64,{data}" height="512" width="512"/>
</svg>
    '''
    resized = resize_image(img, 512)
    buffer = BytesIO()
    resized.save(buffer, format="PNG")
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    svg_data = svg_template.format(data=b64_data)
    with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
        f.write(svg_data)


def save_manifest():
    manifest = {
        "name": "Web App",
        "icons": [
            {
                "src": f"/{OUTPUT_DIR}/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": f"/{OUTPUT_DIR}/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"
    }
    with open(os.path.join(OUTPUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


def gzip_all_files():
    for fname in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, fname)
        if os.path.isfile(path):
            gz_path = path + ".gz"
            with open(path, "rb") as f_in:
                with gzip.open(gz_path, "wb", compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)


def generate_icons(source_image_path, crop_enabled=True):
    if not os.path.isfile(source_image_path):
        raise FileNotFoundError(f"Error: File '{source_image_path}' not found.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img = Image.open(source_image_path).convert("RGBA")
    if crop_enabled:
        img = crop_to_square(img)

    for size, filename, fmt in ICON_SPECS:
        save_png(img, size, filename)

    save_ico(img, ICO_SIZES)
    save_svg_with_png(img)
    save_manifest()
    gzip_all_files()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_icons.py your_image.png [--no-crop]")
        sys.exit(1)

    input_file = sys.argv[1]
    crop = "--no-crop" not in sys.argv[2:]
    try:
        generate_icons(input_file, crop_enabled=crop)
        print("✅ Icons generated successfully in the 'favicons/' folder.")
    except Exception as e:
        print(f"❌ Error: {e}")
