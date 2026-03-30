"""
Tests for core/editor.py
"""

import os
import pytest
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas as rl_canvas


def _make_pdf(tmp_path: Path, pages: int = 3, text: str = "Hello") -> str:
    path = str(tmp_path / "test.pdf")
    c = rl_canvas.Canvas(path)
    for i in range(pages):
        c.drawString(72, 700, f"{text} page {i + 1}")
        c.showPage()
    c.save()
    return path


def _make_image(tmp_path: Path, name: str = "img.png") -> str:
    path = str(tmp_path / name)
    Image.new("RGB", (50, 50), color=(0, 128, 255)).save(path)
    return path


# ---------------------------------------------------------------------------
# add_text_to_page
# ---------------------------------------------------------------------------

def test_add_text_creates_file(tmp_path):
    from src.core.editor import add_text_to_page
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "out.pdf")
    result = add_text_to_page(pdf, out, 0, "Test text", 100, 100)
    assert result == out
    assert os.path.isfile(out)


def test_add_text_invalid_page(tmp_path):
    from src.core.editor import add_text_to_page
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "out.pdf")
    with pytest.raises(IndexError):
        add_text_to_page(pdf, out, 99, "Text", 100, 100)


def test_add_text_file_not_found(tmp_path):
    from src.core.editor import add_text_to_page
    with pytest.raises(FileNotFoundError):
        add_text_to_page("/nope.pdf", str(tmp_path / "out.pdf"), 0, "x", 0, 0)


# ---------------------------------------------------------------------------
# remove_pages
# ---------------------------------------------------------------------------

def test_remove_pages(tmp_path):
    import fitz
    from src.core.editor import remove_pages
    pdf = _make_pdf(tmp_path, pages=3)
    out = str(tmp_path / "out.pdf")
    remove_pages(pdf, out, [1])  # remove page index 1 (page 2)
    doc = fitz.open(out)
    assert doc.page_count == 2
    doc.close()


def test_remove_pages_out_of_range(tmp_path):
    import fitz
    from src.core.editor import remove_pages
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "out.pdf")
    # Index 99 is out of range but should be silently ignored
    remove_pages(pdf, out, [99])
    doc = fitz.open(out)
    assert doc.page_count == 2
    doc.close()


# ---------------------------------------------------------------------------
# add_blank_page
# ---------------------------------------------------------------------------

def test_add_blank_page_append(tmp_path):
    import fitz
    from src.core.editor import add_blank_page
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "out.pdf")
    add_blank_page(pdf, out, insert_after=-1)
    doc = fitz.open(out)
    assert doc.page_count == 3
    doc.close()


def test_add_blank_page_insert(tmp_path):
    import fitz
    from src.core.editor import add_blank_page
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "out.pdf")
    add_blank_page(pdf, out, insert_after=0)
    doc = fitz.open(out)
    assert doc.page_count == 3
    doc.close()


# ---------------------------------------------------------------------------
# reorder_pages
# ---------------------------------------------------------------------------

def test_reorder_pages(tmp_path):
    import fitz
    from src.core.editor import reorder_pages
    pdf = _make_pdf(tmp_path, pages=3)
    out = str(tmp_path / "out.pdf")
    reorder_pages(pdf, out, [2, 0, 1])
    doc = fitz.open(out)
    assert doc.page_count == 3
    doc.close()


# ---------------------------------------------------------------------------
# insert_image_on_page / add_signature
# ---------------------------------------------------------------------------

def test_insert_image_on_page(tmp_path):
    from src.core.editor import insert_image_on_page
    pdf = _make_pdf(tmp_path, pages=1)
    img = _make_image(tmp_path)
    out = str(tmp_path / "out.pdf")
    result = insert_image_on_page(pdf, out, 0, img, (50, 50, 200, 200))
    assert os.path.isfile(result)


def test_add_signature(tmp_path):
    from src.core.editor import add_signature
    pdf = _make_pdf(tmp_path, pages=1)
    img = _make_image(tmp_path)
    out = str(tmp_path / "out.pdf")
    result = add_signature(pdf, out, 0, img, (50, 700, 250, 800))
    assert os.path.isfile(result)
