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

To install Pillow:
    python3 -m pip install --upgrade Pillow

-----------------------------------------------------------
USAGE INSTRUCTIONS
-----------------------------------------------------------
1. Place your source image (PNG format recommended, 512x512 or larger) in the same folder.

2. Run the script using:
       python3 generate_icons.py <your-image.png>

   Example:
       python3 generate_icons.py MyImage.png

3. The script will:
    ✓ Create a "favicons/" directory (if not already present)
    ✓ Resize and generate all required icon sizes (PNG and ICO)
    ✓ Create a Safari pinned-tab icon (SVG)
    ✓ Create a PWA manifest.json
    ✓ Gzip all generated files (*.gz) without deleting originals

-----------------------------------------------------------
FEATURES
-----------------------------------------------------------
✓ PNG icons for:
   - Standard browser tabs (16x16, 32x32, 48x48)
   - iOS devices (72x72 to 180x180)
   - Android/Chrome (192x192, 512x512)
   - Windows tiles (70x70 to 310x310)
   - Chrome Web Store (128x128)
✓ Multi-resolution favicon.ico (16–256 px)
✓ manifest.json for PWA apps
✓ Safari pinned-tab icon (SVG with base64 PNG)
✓ Gzip compression (level 9) of all output files
✓ Source image is supplied as a command-line argument

-----------------------------------------------------------
EXAMPLE OUTPUT
-----------------------------------------------------------
/favicons/
├── android-chrome-192x192.png
├── apple-touch-icon-120x120.png
├── favicon-16x16.png
├── favicon.ico
├── safari-pinned-tab.svg
├── manifest.json
├── favicon-16x16.png.gz
├── manifest.json.gz
└── ... (and more .png/.gz files)

-----------------------------------------------------------
HTML HEAD SNIPPET
-----------------------------------------------------------
Include this in your <head> section:

<link rel="icon" type="image/png" sizes="16x16" href="favicons/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="favicons/favicon-32x32.png">
<link rel="shortcut icon" href="favicons/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="favicons/apple-touch-icon-180x180.png">
<link rel="manifest" href="favicons/manifest.json">
<link rel="mask-icon" href="favicons/safari-pinned-tab.svg" color="#000000">
<meta name="theme-color" content="#ffffff">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="favicons/mstile-150x150.png">

-----------------------------------------------------------
SERVER RECOMMENDATIONS
-----------------------------------------------------------
- Serve .gz files using proper Content-Encoding headers if supported
- Use long cache expiration (e.g. max-age=31536000) for icons
- Ensure MIME types are correct (e.g., .svg = image/svg+xml, .json = application/json)

-----------------------------------------------------------
LICENSE
-----------------------------------------------------------
This script is provided as-is with no warranty. You may modify and redistribute freely.
