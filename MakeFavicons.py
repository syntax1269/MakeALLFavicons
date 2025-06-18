import sys
import os
from PIL import Image
import base64
import json
import gzip
import shutil

# === GET INPUT FILE FROM COMMAND LINE ===
if len(sys.argv) != 2:
    print("Usage: python3 generate_icons.py <source_image.png>")
    sys.exit(1)

input_image_path = sys.argv[1]

if not os.path.isfile(input_image_path):
    print(f"Error: '{input_image_path}' not found.")
    sys.exit(1)


output_dir = "favicons"
os.makedirs(output_dir, exist_ok=True)

# === ICON DEFINITIONS ===
icon_specs = [
    (16,  "favicon-16x16.png"),
    (32,  "favicon-32x32.png"),
    (48,  "favicon-48x48.png"),
    (72,  "apple-touch-icon-72x72.png"),
    (76,  "apple-touch-icon-76x76.png"),
    (114, "apple-touch-icon-114x114.png"),
    (120, "apple-touch-icon-120x120.png"),
    (128, "favicon-128x128.png"),
    (144, "android-chrome-144x144.png"),
    (152, "apple-touch-icon-152x152.png"),
    (167, "apple-touch-icon-167x167.png"),
    (180, "apple-touch-icon-180x180.png"),
    (192, "android-chrome-192x192.png"),
    (256, "favicon-256x256.png"),
    (512, "android-chrome-512x512.png"),
    (70,  "mstile-70x70.png"),
    (150, "mstile-150x150.png"),
    (310, "mstile-310x310.png"),
    ((310, 150), "mstile-310x150.png")
]

# === LOAD IMAGE ===
img = Image.open(input_image_path)

# === GENERATE PNG ICONS ===
generated_files = []
for size, filename in icon_specs:
    if isinstance(size, tuple):
        resized = img.resize(size, Image.LANCZOS)
    else:
        resized = img.resize((size, size), Image.LANCZOS)
    filepath = os.path.join(output_dir, filename)
    resized.save(filepath, format="PNG")
    generated_files.append(filepath)
    print(f"Saved: {filename}")

# === SAVE MULTI-RESOLUTION ICO ===
ico_path = os.path.join(output_dir, "favicon.ico")
ico_sizes = [(s, s) for s in [16, 32, 48, 64, 128, 256]]
img.save(ico_path, format="ICO", sizes=ico_sizes)
generated_files.append(ico_path)
print("Saved: favicon.ico")

# === CREATE SVG FOR SAFARI PINNED TAB ===
svg_path = os.path.join(output_dir, "safari-pinned-tab.svg")
with open(input_image_path, "rb") as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512">
  <image href="data:image/png;base64,{image_base64}" height="512" width="512"/>
</svg>'''

with open(svg_path, "w") as f:
    f.write(svg_content)
generated_files.append(svg_path)
print("Saved: safari-pinned-tab.svg")

# === GENERATE manifest.json ===
manifest = {
    "name": "My Web App",
    "short_name": "App",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#ffffff",
    "icons": [
        {
            "src": "android-chrome-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "android-chrome-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
manifest_path = os.path.join(output_dir, "manifest.json")
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)
generated_files.append(manifest_path)
print("Saved: manifest.json")

# === GZIP ALL GENERATED FILES ===
print("\n🔧 Gzipping all files...")
for file_path in generated_files:
    gz_path = file_path + ".gz"
    with open(file_path, "rb") as f_in:
        with gzip.open(gz_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Gzipped: {os.path.basename(gz_path)}")

print("\n✅ All icons, manifest.json, and .gz versions generated successfully.")
