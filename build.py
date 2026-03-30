"""
Build script for PDF Solutions Desktop Application.
Bundles the app into a standalone .exe using PyInstaller.

Usage:
    python build.py
"""

import os
import sys
import PyInstaller.__main__

# Use the correct path separator for the current platform
SEP = ";" if sys.platform == "win32" else ":"

# Resolve the project root (directory containing this script)
ROOT = os.path.dirname(os.path.abspath(__file__))

assets_src = os.path.join(ROOT, "assets")
src_src = os.path.join(ROOT, "src")

PyInstaller.__main__.run([
    os.path.join(ROOT, "main.py"),
    "--name=PDF_Solutions",
    "--onefile",
    "--windowed",
    f"--add-data={assets_src}{SEP}assets",
    f"--add-data={src_src}{SEP}src",
    "--hidden-import=PySide6.QtCore",
    "--hidden-import=PySide6.QtGui",
    "--hidden-import=PySide6.QtWidgets",
    "--hidden-import=PySide6.QtSvg",
    "--hidden-import=PySide6.QtPrintSupport",
    "--hidden-import=fitz",
    "--hidden-import=pymupdf",
    "--hidden-import=reportlab",
    "--hidden-import=reportlab.lib",
    "--hidden-import=reportlab.lib.pagesizes",
    "--hidden-import=reportlab.pdfgen",
    "--hidden-import=reportlab.pdfgen.canvas",
    "--hidden-import=openpyxl",
    "--hidden-import=docx",
    "--hidden-import=pikepdf",
    "--hidden-import=PIL",
    "--hidden-import=PIL.Image",
    "--hidden-import=pypdf",
    "--clean",
    "--noconfirm",
])
