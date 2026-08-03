# OptiPixel 🖼️⚡ (راهنمای فارسی)

**اپتی‌پیکسل (OptiPixel)** یک نرم‌افزار دسکتاپ و ابزار وب قدرتمند برای بهینه‌سازی گروهی تصاویر، تبدیل فرمت‌ها و ممیزی سرعت صفحات وب‌سایت است که با **پایتون (PySide6)** و موتور قدرتمند **ImageMagick 7** طراحی شده است.

زبان‌ها: [English](README.md) | [فارسی](README.fa.md)

---

## 📥 دانلود و استفاده از نسخه منتشر شده (Release)

برای دانلود و استفاده از نسخه آماده اجرای دسکتاپ روی ویندوز:

۱. آخرین نسخه فایل نصب‌کننده `OptiPixel-Installer.exe` را از بخش [انتشارهای گیت‌هاب (Releases)](https://github.com/h08831n/OptiPixel/releases) دریافت کنید.
۲. فایل `OptiPixel-Installer.exe` را اجرا کرده و مراحل نصب را طی کنید.
۳. نرم‌افزار **OptiPixel** را از منوی استارت یا شورت‌کات دسکتاپ اجرا نمایید.

---

## 🛠️ تکنولوژی‌های استفاده‌شده

- **رابط کاربری (GUI)**: PySide6 (Qt6 برای پایتون) و React 19 + TypeScript + Tailwind CSS
- **موتور پردازش تصویر**: نسخه ۷ موتور قدرتمند ImageMagick (کدک‌های وب‌پی، ای‌وی‌آی‌اف، جی‌پگ، پی‌ان‌جی، تیف و بی‌ام‌پی)
- **سرور رابط وب**: Node.js و Express.js
- **بسته‌بندی و کامپایل**: PyInstaller و Inno Setup (سازنده فایل نصب ویندوز)

---

## 💻 راهنمای توسعه و اجرای سورس کد

### ۱. پیش‌نیازها
- پایتون نسخه ۳.۱۰ یا بالاتر
- Node.js نسخه ۱۸ یا بالاتر (جهت بخش وب)
- نرم‌افزار ImageMagick نسخه ۷ افزوده شده به PATH سیستم (`magick` یا `convert`)

### ۲. اجرای برنامه پایتون (Desktop)
```bash
# دریافت ریپازیتوری
git clone https://github.com/h08831n/OptiPixel.git
cd OptiPixel

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای نرم‌افزار
python -m app.main
```
یا در محیط PowerShell ویندوز:
```powershell
.\run.ps1
```

### ۳. اجرای محیط وب (Web Interface)
```bash
# نصب پکیج‌های نود
npm install

# اجرای سرور توسعه
npm run dev
```

### ۴. ساخت فایل اجرایی (Build)
برای کامپایل نسخه دسکتاپ و فایل نصب‌کننده ویندوز:
```powershell
.\build.ps1
```
فایل‌های خروجی در پوشه `dist/` ساخته خواهند شد.

---

## ☕ حمایت مالی (Crypto Donation)

اگر نرم‌افزار OptiPixel برای شما مفید بوده است، می‌توانید از توسعه آن حمایت کنید:

- **آدرس کیف پول TON / USDT (شبکه TON)**:
  `UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3`

---

## 🐛 گزارش باگ و پیشنهادات (Bug Report)

در صورت مشاهده هرگونه مشکل یا پیشنهاد برای بهبود، لطفاً یک گزارش در بخش Issue‌های گیت‌هاب ثبت کنید:
[https://github.com/h08831n/OptiPixel/issues](https://github.com/h08831n/OptiPixel/issues)

---

## 📜 مجوز
توسعه یافته توسط **h08831n** تحت مجوز MIT
