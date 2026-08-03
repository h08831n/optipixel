# OptiPixel

**Web Image Optimizer & Converter**

![OptiPixel Banner](assets/images/banner.png)

OptiPixel is a high-performance Windows desktop application and web solution for optimizing, compressing, and converting web images in bulk. It is specifically designed for website owners, WordPress administrators, digital creators, and media production teams who handle large image libraries.

---

## 🌟 Key Features

- **⚡ ImageMagick 7.x Integration:** Uses native `magick` CLI for high-speed, lossy and lossless image compression.
- **🖼️ Comprehensive Format Support:** WebP, AVIF, HEIC, JPEG XL, JPEG, PNG, TIFF, BMP, and GIF.
- **📂 Batch & Recursive Processing:** Process thousands of images across complex subfolder hierarchies with zero UI freezing.
- **🛡️ Atomic Safety Engine:** Processes to temporary files first, validates dimension and size, and preserves backups before overwriting originals.
- **⚙️ Threshold Filtering:** Set file size criteria (e.g., process only images > 400 KB) and automatically keep originals if output is larger.
- **📐 Smart Resizing & Metadata:** Constrain maximum dimensions maintaining aspect ratio (without upscaling) and strip EXIF metadata safely.
- **🌍 Multilingual LTR & RTL Support:** Fully localized in English, فارسی, Deutsch, Türkçe, العربية, Français, Español, and Русский.
- **📊 SEO Image Audit & Reports:** Scan folders for heavy images without modifying files, and export detailed CSV / JSON reports.
- **💻 Desktop & Web Preview:** Build standalone Windows `.exe` using PyInstaller and Inno Setup installer.

---

## 🚀 Quick Start (Development)

### Prerequisites

- Python 3.12+
- ImageMagick 7.x (available via `magick` command in system PATH or custom location)

### Installation

```bash
# Clone the repository
git clone https://github.com/ahaninja/OptiPixel.git
cd OptiPixel

# Create and activate virtual environment
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements-dev.txt
```

### Running the Application

```bash
# Run PySide6 Desktop GUI
python -m app.main

# Run Web Preview Server
npm run dev
```

### Running Tests

```bash
pytest
```

---

## 📦 Building Standalone Executable & Installer

### Build PyInstaller Executable

```powershell
.\build.ps1
```
This script compiles the application using PyInstaller into `dist/OptiPixel/`.

### Generate Windows Installer (Inno Setup)

Requires Inno Setup 6+ (`ISCC.exe`):

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\OptiPixel.iss
```

Output installer: `Output/OptiPixel-Setup-0.1.0.exe`

---

## 🏛️ Project Architecture

```
OptiPixel/
├── app/
│   ├── core/         # Processing engine, optimizer, converter, scanner, output & backup managers
│   ├── workers/      # QThreadPool / QRunnable worker threads & task pools
│   ├── ui/           # PySide6 main window, pages, widgets (LTR/RTL responsive)
│   ├── services/     # ImageMagick CLI detection, settings, history, GitHub updates
│   ├── config/       # Constants, settings schemas, presets, defaults
│   ├── i18n/         # Multilingual translation files (EN, FA, DE, TR, AR, FR, ES, RU)
│   └── utils/        # File, path, size, and logging utilities
├── installer/        # Inno Setup script (OptiPixel.iss)
├── tests/            # PyTest suite for scanner, optimizer, converter, output manager
├── .github/          # CI/CD workflows for automated release build
└── build.ps1         # PowerShell build script
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

**Publisher:** [Ahaninja](https://ahaninja.com)
