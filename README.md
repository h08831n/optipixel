# OptiPixel 🖼️⚡

**OptiPixel** is a high-performance, cross-platform image optimization, batch conversion, and SEO media auditing desktop application built with Python (PySide6) and ImageMagick 7 CLI engine, as well as a modern web interface.

[![GitHub Release](https://img.shields.io/github/v/release/h08831n/OptiPixel)](https://github.com/h08831n/OptiPixel/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)

Languages: [English](README.md) | [فارسی](README.fa.md)

---

## 🌟 Key Features

- **⚡ Batch Image Optimization**: Lossy and Lossless WebP, AVIF, JPEG, PNG, TIFF, and BMP compression.
- **🎯 Smart Threshold Filtering**: Automatically skip images smaller than a configurable threshold (e.g. 400 KB).
- **🛡️ Quality Preservation Guard**: Keeps original files if compressed output happens to be larger.
- **📐 Smart Resizing**: Constrain maximum width and height while maintaining aspect ratio.
- **🏷️ Metadata Control**: Strip unnecessary EXIF data while preserving correct orientation.
- **🔍 SEO & Core Web Vitals Audit**: Read-only directory scanner that highlights heavy web images.
- **💼 Multiple Output Strategies**: Save to a new directory, replace originals with automatic backups, or save alongside source files.
- **❤️ Crypto Donation Support**: Support open-source development directly via TON network crypto transfers.

---

## 📦 How to Build & Publish Releases

### 1. Prerequisites
- Python 3.10+
- ImageMagick 7 (`magick` CLI in PATH)
- Inno Setup 6 (for Windows installer `.exe` creation)

### 2. Local Build Script (Windows)
Run PowerShell build script:
```powershell
.\build.ps1
```
This compiles `app/main.py` into a single standalone executable using PyInstaller and packages it into `OptiPixel-Installer.exe` using Inno Setup (`installer/OptiPixel.iss`).

### 3. Creating a GitHub Release
1. Tag your repository with the version number:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```
2. Go to `https://github.com/h08831n/OptiPixel/releases/new`
3. Select `v0.1.0` tag, enter Release Title and Changelog notes.
4. Upload `OptiPixel-Installer.exe` and `OptiPixel-Standalone.zip` from `dist/` build directory.
5. Publish Release!

---

## ☕ Support & Crypto Donation

If OptiPixel saved you bandwidth or time, consider supporting development:

- **TON / USDT (TON Network) Wallet Address**:
  `UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3`

---

## 🐛 Bug Reports & Feedback

Found an issue or have a feature request?
Submit a report on GitHub Issues: [https://github.com/h08831n/OptiPixel/issues](https://github.com/h08831n/OptiPixel/issues)

---

## 📜 License
MIT License - Developed by **h08831n**
