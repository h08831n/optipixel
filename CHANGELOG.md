# Changelog - OptiPixel

All notable changes to OptiPixel will be documented in this file.

## [0.1.0] - 2026-08-03

### Initial Release
- **Core Engine:**
  - Automated ImageMagick 7.x detection (`magick` CLI) with fallback to custom path.
  - Image format capability scanner (WebP, AVIF, HEIC, JPEG XL, JPEG, PNG, TIFF, BMP).
  - Multi-threaded batch processor with QThreadPool workers, pause/resume/cancel support.
- **Optimization Features:**
  - Lossy & Lossless WebP optimization.
  - AVIF, JPEG, PNG, TIFF compression controls.
  - Configurable file size threshold filter (default 400 KB).
  - "Keep original if output is larger" safety mechanism.
  - Optional dimension resizing with aspect ratio preservation (no upscaling).
  - Metadata stripping option preserving orientation and color profiles.
- **Output Management & Safety:**
  - 3 Output Modes: Replace Original, Save to Another Folder, Save Next to Original.
  - Atomic replacement via temporary files and verification checks.
  - Automated folder structure preservation and backup system (`.backup` or timestamped folders).
- **User Interface (PySide6 & Web GUI):**
  - Modern dark/light/system responsive UI.
  - Drag and drop file & recursive subfolder import.
  - Live progress display with current file progress, overall stats, and speed.
  - Multilingual support: English, فارسی (Persian), Deutsch, Türkçe, العربية, Français, Español, Русский with dynamic LTR/RTL layout direction switching.
- **Audit & Analytics:**
  - Read-only SEO/Web Performance Folder Audit with size brackets (>400KB, >1MB, >2MB, >5MB).
  - Exportable job reports in CSV and JSON formats.
  - Job History viewer with space-saved stats.
- **Deployment & Distribution:**
  - PyInstaller build configuration for Windows `.exe`.
  - Inno Setup installer script (`OptiPixel.iss`).
  - GitHub Actions automated release pipeline (`release.yml`).
