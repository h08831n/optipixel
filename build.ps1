# OptiPixel Windows Build Script
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Building OptiPixel Desktop Application " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check Virtual Environment
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "[1/5] Virtual environment not found, using global Python..." -ForegroundColor Yellow
}

# Install Dependencies
Write-Host "[2/5] Checking dependencies..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

# Run Tests
Write-Host "[3/5] Running test suite..." -ForegroundColor Green
python -m pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed! Aborting build." -ForegroundColor Red
    exit 1
}

# Run PyInstaller
Write-Host "[4/5] Building PyInstaller executable..." -ForegroundColor Green
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

python -m PyInstaller `
    --name="OptiPixel" `
    --windowed `
    --noconfirm `
    --clean `
    --icon="assets/icons/app_icon.ico" `
    --add-data="app/i18n;app/i18n" `
    --add-data="assets;assets" `
    --add-data="VERSION;." `
    app/main.py

Write-Host "[5/5] Build complete! Executable located in dist/OptiPixel/OptiPixel.exe" -ForegroundColor Green
