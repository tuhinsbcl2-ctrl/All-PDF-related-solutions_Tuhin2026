# PDF Solutions Desktop Application

> **All-in-one PDF toolkit for desktop** — built with Python & PySide6 (Qt6)

![PDF Solutions Desktop App](https://github.com/user-attachments/assets/8370d3a6-2a8d-4a35-8483-4292cfbe23a9)

## ✨ Features

| Category | Feature |
|---|---|
| **Convert** | PDF → Excel, Excel → PDF, PDF → Word, Word → PDF, Photos → PDF, PDF → Photos |
| **Edit** | Add text, Add images/signatures, Remove pages, Add blank pages, Reorder pages |
| **Compress** | Low / Medium / High compression with before/after size stats |
| **Security** | Lock PDF (AES-256), Unlock PDF |
| **Page Numbers** | Configurable position, font size, start number, prefix/suffix |
| **Organize** | Merge, Split, Rotate, Crop, Repair, Visual page reorder |
| **Watermark** | Add text watermark, Add image watermark, Remove text watermark |

## 🚀 Installation & Usage

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/tuhinsbcl2-ctrl/All-PDF-related-solutions_Tuhin2026.git
cd All-PDF-related-solutions_Tuhin2026

# Install dependencies
pip install -r requirements.txt

# Launch the app
python main.py
```

### Option 2: Build a Standalone `.exe` (Windows)

Build a single `PDF_Solutions.exe` that runs without Python installed.

**Easiest way — double-click `build_exe.bat`:**

1. Make sure Python is installed on your machine.
2. Double-click **`build_exe.bat`** in the project folder.
3. Wait for the build to finish — it will create `dist\PDF_Solutions.exe`.
4. Double-click `dist\PDF_Solutions.exe` to launch the app! 🎉

**Or run the build script manually:**

```bash
pip install pyinstaller
python build.py
# Output: dist/PDF_Solutions.exe
```

### Option 3: Download a Pre-built Release

Check the [Releases](https://github.com/tuhinsbcl2-ctrl/All-PDF-related-solutions_Tuhin2026/releases) page for a ready-to-use `PDF_Solutions.exe` (built automatically by GitHub Actions on every version tag).

## 🛠 Tech Stack

| Component | Library |
|---|---|
| GUI Framework | PySide6 (Qt6) |
| PDF reading/rendering | PyMuPDF (fitz) |
| PDF manipulation | pypdf |
| PDF generation | reportlab |
| Image processing | Pillow |
| Excel handling | openpyxl |
| Word documents | python-docx |
| PDF encryption | pikepdf |
| Testing | pytest |

## 📁 Project Structure

```
├── main.py                  # Entry point
├── requirements.txt
├── setup.py
├── src/
│   ├── app.py               # QApplication setup
│   ├── ui/
│   │   ├── main_window.py   # Sidebar + all feature pages
│   │   ├── home_page.py     # Dashboard with feature cards
│   │   ├── styles.py        # Dark/light QSS themes
│   │   └── widgets/
│   │       ├── file_drop_widget.py
│   │       ├── progress_widget.py
│   │       └── preview_widget.py
│   ├── core/
│   │   ├── converter.py     # PDF↔Excel, PDF↔Word, Photo↔PDF
│   │   ├── editor.py        # Text/image/page editing
│   │   ├── compressor.py    # PDF compression
│   │   ├── security.py      # Lock/unlock (pikepdf)
│   │   ├── organizer.py     # Merge/split/rotate/crop/reorder
│   │   ├── watermark.py     # Add/remove watermarks
│   │   ├── repair.py        # PDF repair
│   │   └── page_numbers.py  # Add page numbers
│   └── utils/
│       ├── file_utils.py
│       └── pdf_utils.py
└── tests/
    ├── test_converter.py
    ├── test_editor.py
    ├── test_compressor.py
    ├── test_security.py
    └── test_organizer.py
```

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
