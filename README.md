# OptiPixel 🖼️⚡ (v1.0.0)

**OptiPixel** is a high-performance image optimization, batch format converter, and web media auditing tool. Built with **Python (PySide6)** and **ImageMagick 7**, accompanied by a modern React web interface.

[![GitHub Repository](https://img.shields.io/badge/GitHub-h08831n%2FOptiPixel-blue?logo=github)](https://github.com/h08831n/OptiPixel)
[![GitHub Release](https://img.shields.io/github/v/release/h08831n/OptiPixel?color=emerald)](https://github.com/h08831n/OptiPixel/releases/latest)
[![Version](https://img.shields.io/badge/version-1.0.0-indigo.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)

Languages: [English](README.md) | [فارسی](README.fa.md)

---

## 🚀 What's New in Version 1.0.0

- 🎨 **IRANYekanX Typography**: Integrated premium **IRANYekanX** font for high-legibility Persian/Arabic and English UI rendering.
- ⚡ **Silent Background Execution**: ImageMagick background conversions now run with suppressed terminal windows (`CREATE_NO_WINDOW`) so no Command Prompt popups interrupt your workflow.
- 🔄 **In-App Direct Auto-Update**: Built-in auto-update system that downloads the installer package directly with a progress bar and installs it seamlessly inside the app.
- 📦 **Unified Full Feature Set**: Consolidates image compression, batch conversion, web site auditing, history tracking, FTP uploads, and backup management into a stable `v1.0.0` release.

---

## 📥 Download Latest Release

Get the latest installer from the official release page:

👉 **[Download OptiPixel v1.0.0 Latest Release](https://github.com/h08831n/OptiPixel/releases/latest)**

1. Download `OptiPixel-Setup-1.0.0.exe` or `OptiPixel-Installer.exe` from [GitHub Releases Latest](https://github.com/h08831n/OptiPixel/releases/latest).
2. Run the installer to setup OptiPixel on Windows.
3. Launch **OptiPixel** from your Start Menu or Desktop shortcut.

---

## ✨ Features Overview

- ⚡ **Batch Image Optimization**: Compress WebP, AVIF, JPEG, PNG, HEIC, TIFF, and BMP with smart quality & size target controls.
- 🔄 **Format Converter**: Instant multi-format conversion with subfolder structure preservation.
- 📐 **Resize & Metadata Stripper**: Custom dimension scaling and EXIF data removal for smaller payload sizes.
- 🌐 **Web Page Auditor**: Crawl web URLs to inspect image sizes, formats, and estimate potential bandwidth savings.
- 🛰️ **FTP Integration**: Automatically upload converted or optimized images directly to remote web servers.
- 📊 **History & Statistics**: Keep track of disk space saved, compression ratio history, and processed file records.

---

## 🛠️ Stack & Technologies Used

- **GUI Engine**: PySide6 (Qt for Python 6) & React 19 + TypeScript + Tailwind CSS
- **Typography**: IRANYekanX & Vazirmatn
- **Processing Core**: ImageMagick 7 CLI engine (High-speed WebP, AVIF, JPEG, PNG, TIFF, BMP codecs)
- **Backend API Server**: Node.js & Express.js
- **Packaging**: PyInstaller & Inno Setup (Windows installer builder)

---

## 💻 Development & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher (for Web UI)
- ImageMagick 7 installed in system PATH (`magick` or `convert` CLI command)

### 2. Running Desktop Application
```bash
git clone https://github.com/h08831n/OptiPixel.git
cd OptiPixel

pip install -r requirements.txt
python -m app.main
```
Or run via PowerShell on Windows:
```powershell
.\run.ps1
```

### 3. Running Web Interface
```bash
npm install
npm run dev
```

### 4. Building Executable & Installer
To compile the standalone Windows executable and Inno Setup installer:
```powershell
.\build.ps1
```

---

## ☕ Support & Crypto Donation

If OptiPixel saved you bandwidth or processing time, consider supporting development:

- **TON / USDT (TON Network) Wallet**:
  `UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3`

---

## 📜 License
MIT License - Developed by **h08831n**
