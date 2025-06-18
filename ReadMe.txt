---

# 🧰 Favicon Generator Script

This Python script automates the creation of a complete set of favicon and application icons from a single high-resolution image. It supports virtually all modern platforms including:

* ✅ Web browsers (PNG, ICO, SVG)
* ✅ Apple iOS/iPadOS (touch icons)
* ✅ Android (PWA and homescreen)
* ✅ Microsoft Windows tiles
* ✅ Progressive Web App (PWA) manifest
* ✅ Gzipped assets for performance

---

## 📦 Features

* Generates **20+ icon sizes**
* Outputs in `.png`, `.ico`, and `.svg` formats
* Auto-generates a `manifest.json` for web apps
* Automatically **crops** to square (optional)
* Gzips all output files using **maximum compression** (`gzip -9`)
* Organizes everything into a `favicons/` folder
* Supports command-line flags for automation

---

## ⚙️ Requirements

* Python **3.6+**
* [Pillow](https://pypi.org/project/Pillow/) (PIL fork)

### Installation:

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install Pillow
```

---

## 🚀 Usage

### Basic Command:

```bash
python3 generate_icons.py my_logo.png
```

### Optional Flags:

* `--no-crop` → Disables automatic square cropping

### Example:

```bash
python3 generate_icons.py my_logo.png --no-crop
```

---

## 🖼️ Input Image Guidelines

* Format: PNG (preferred), JPEG also supported
* Resolution: **At least 512×512 px**
* Aspect Ratio: **Square recommended**
* Transparency: Recommended for `.ico` and `.svg`

---

## 📁 Output Files

All generated files are saved in the `favicons/` directory.

### 🔹 Standard Favicons

| Size      | Format | File                    |
| --------- | ------ | ----------------------- |
| 16×16     | PNG    | `favicon-16x16.png`     |
| 32×32     | PNG    | `favicon-32x32.png`     |
| 48×48     | PNG    | `favicon-48x48.png`     |
| 128×128   | PNG    | `favicon-128x128.png`   |
| 256×256   | PNG    | `favicon-256x256.png`   |
| Multi-res | ICO    | `favicon.ico`           |
| Vector    | SVG    | `safari-pinned-tab.svg` |

### 🍏 Apple Touch Icons (iOS/iPadOS)

| Size    | File                           |
| ------- | ------------------------------ |
| 72×72   | `apple-touch-icon-72x72.png`   |
| 76×76   | `apple-touch-icon-76x76.png`   |
| 114×114 | `apple-touch-icon-114x114.png` |
| 120×120 | `apple-touch-icon-120x120.png` |
| 152×152 | `apple-touch-icon-152x152.png` |
| 167×167 | `apple-touch-icon-167x167.png` |
| 180×180 | `apple-touch-icon-180x180.png` |

### 🤖 Android & PWA

| Size     | File                         |
| -------- | ---------------------------- |
| 144×144  | `android-chrome-144x144.png` |
| 192×192  | `android-chrome-192x192.png` |
| 512×512  | `android-chrome-512x512.png` |
| Manifest | `manifest.json`              |

### 🪟 Windows Tiles

| Size    | File                 |
| ------- | -------------------- |
| 70×70   | `mstile-70x70.png`   |
| 150×150 | `mstile-150x150.png` |
| 310×150 | `mstile-310x150.png` |
| 310×310 | `mstile-310x310.png` |

### 🔐 Gzipped Versions

Each output file is also compressed with gzip using `gzip -9`, producing:

```txt
favicon-32x32.png
favicon-32x32.png.gz
...
```

---

## 🌐 HTML Integration Example

Include the following tags in your `<head>` section:

```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicons/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicons/apple-touch-icon-180x180.png">
<link rel="manifest" href="/favicons/manifest.json">
<link rel="mask-icon" href="/favicons/safari-pinned-tab.svg" color="#5bbad5">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="msapplication-TileImage" content="/favicons/mstile-144x144.png">
<meta name="theme-color" content="#ffffff">
```

---

## 🛑 Error Handling

* If the image path is invalid or unreadable, the script will exit with an error.
* Make sure the source image is present and accessible.

---

## 🗂️ File Structure Example

```
your_project/
├── generate_icons.py
├── my_logo.png
└── favicons/
    ├── favicon-16x16.png
    ├── favicon-32x32.png
    ├── ...
    ├── safari-pinned-tab.svg
    ├── manifest.json
    ├── favicon-32x32.png.gz
    └── ...
```

---

## 📄 License

This script is open-source under the **MIT License**.
Feel free to use, modify, and distribute. Attribution is appreciated but not required.

---
