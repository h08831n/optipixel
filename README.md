# OptiPixel 🖼️⚡

**OptiPixel** is a high-performance image optimization, batch converter, and web media auditing tool. Built with **Python (PySide6)** and **ImageMagick 7**, along with a modern web dashboard.

[![GitHub Repository](https://img.shields.io/badge/GitHub-h08831n%2FOptiPixel-blue?logo=github)](https://github.com/h08831n/OptiPixel)
[![GitHub Release](https://img.shields.io/github/v/release/h08831n/OptiPixel?color=emerald)](https://github.com/h08831n/OptiPixel/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)

Languages: [English](README.md) | [فارسی](README.fa.md)

---

## 📥 Download & Usage (Released Version)

To use the pre-compiled, ready-to-run desktop version on Windows:

1. Download the latest installer `OptiPixel-Installer.exe` from [GitHub Releases](https://github.com/h08831n/OptiPixel/releases).
2. Run `OptiPixel-Installer.exe` to install OptiPixel on your machine.
3. Launch **OptiPixel** from your Start Menu or Desktop shortcut.

---

## 🛠️ Stack & Technologies Used

- **GUI Engine**: PySide6 (Qt for Python 6) & React 19 + TypeScript + Tailwind CSS
- **Processing Core**: ImageMagick 7 CLI engine (High-speed WebP, AVIF, JPEG, PNG, TIFF, BMP codecs)
- **Backend API Server**: Node.js & Express.js (Local runner bridge)
- **Packaging**: PyInstaller & Inno Setup (Windows installer generator)

---

## 💻 Development & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher (for Web UI)
- ImageMagick 7 installed in system PATH (`magick` or `convert` CLI command)

### 2. Running Python Desktop App
```bash
# Clone the repository
git clone https://github.com/h08831n/OptiPixel.git
cd OptiPixel

# Install dependencies (Standard library urllib is used for network calls)
pip install -r requirements.txt

# Run application
python -m app.main
```
Or use the PowerShell runner script on Windows:
```powershell
.\run.ps1
```

### 3. Running Web Interface
```bash
# Install node packages
npm install

# Start local dev server
npm run dev
```

### 4. Building Executable & Installer
To compile the standalone Windows `.exe` and installer:
```powershell
.\build.ps1
```
The compiled output will be generated inside the `dist/` directory.

---

## ☕ Support & Crypto Donation

If OptiPixel saved you bandwidth or time, consider supporting ongoing development:

- **TON / USDT (TON Network) Wallet Address**:
  `UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3`

---

## 🐛 Bug Reports & Feedback

Found an issue or have a feature request? Submit a report on GitHub:
[https://github.com/h08831n/OptiPixel/issues](https://github.com/h08831n/OptiPixel/issues)

---

## 📜 License
MIT License - Developed by **h08831n**
