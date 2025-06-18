FAVICON & APP ICON GENERATOR WITH GZIP + MANIFEST SUPPORT
===========================================================

This Python script generates a complete set of favicons and app icons for web apps,
iOS, Android, and Windows tiles. It resizes a single source image into various formats 
and dimensions, creates an app manifest.json file, a Safari-pinned tab icon (SVG),
and gzips all the output files while preserving the originals.

-----------------------------------------------------------
REQUIREMENTS
-----------------------------------------------------------
- Python 3.7 or newer
- [Pillow] Python Imaging Library for image resizing

Install Pillow using pip (Python package manager):
    python3 -m pip install --upgrade Pillow

-----------------------------------------------------------
USAGE INSTRUCTIONS
-----------------------------------------------------------
1. Place your source image in the same folder as the script
   (Recommended: Transparent PNG, at least 512x512 pixels)

2. Update this line(9) in the script of your image:
       input_image_path = "<SOURCE FILENAME HERE>"

3. Run the script using:
       python3 generate_icons.py

4. The script will:
    - Create a "favicons" directory
    - Generate all icon sizes in PNG and ICO formats
    - Generate a Safari-compatible pinned tab SVG
    - Generate a PWA-compatible manifest.json
    - Gzip every output file (leaving the originals intact)

5. Upload the contents of the "favicons" folder to your web root
   and include the provided <head> HTML snippet in your website's <head> section.

-----------------------------------------------------------
FEATURES
-----------------------------------------------------------
✓ Supports all major favicon and app icon sizes:
    - Browser tabs, iOS home screens, Android launchers, Windows tiles, Chrome apps

✓ Generates:
    - .png files (16x16 to 512x512)
    - .ico file (multi-resolution)
    - .svg Safari-pinned tab icon
    - manifest.json (with Android-compatible icons)
    - Gzipped versions of all assets (.gz)

✓ Includes pre-generated HTML <head> snippet for fast integration

-----------------------------------------------------------
FILE STRUCTURE
-----------------------------------------------------------
/favicons/
    favicon-16x16.png
    favicon-32x32.png
    ...
    apple-touch-icon-180x180.png
    safari-pinned-tab.svg
    manifest.json
    favicon.ico
    (plus .gz versions of each)

-----------------------------------------------------------
SUPPORT & TIPS
-----------------------------------------------------------
- Ensure all files are served with appropriate MIME types and
  enable gzip encoding on your web server to use .gz versions.
- Always include <link rel="manifest"> and <meta name="theme-color"> for PWA support.
- Apple requires exact icon sizes, so do not resize dynamically via CSS or HTML.

-----------------------------------------------------------
LICENSE
-----------------------------------------------------------
This script is provided as-is with no warranty. You may modify and redistribute freely.
