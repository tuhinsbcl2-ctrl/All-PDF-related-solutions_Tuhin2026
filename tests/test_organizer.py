"""
Tests for core/organizer.py
"""

import os
import pytest
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
import fitz


def _make_pdf(tmp_path: Path, name: str = "test.pdf", pages: int = 3) -> str:
    path = str(tmp_path / name)
    c = rl_canvas.Canvas(path)
    for i in range(pages):
        c.drawString(72, 700, f"Page {i + 1}")
        c.showPage()
    c.save()
    return path


# ---------------------------------------------------------------------------
# merge_pdfs
# ---------------------------------------------------------------------------

def test_merge_pdfs(tmp_path):
    from src.core.organizer import merge_pdfs
    pdf1 = _make_pdf(tmp_path, "a.pdf", pages=2)
    pdf2 = _make_pdf(tmp_path, "b.pdf", pages=3)
    out = str(tmp_path / "merged.pdf")
    result = merge_pdfs([pdf1, pdf2], out)
    assert result == out
    doc = fitz.open(out)
    assert doc.page_count == 5
    doc.close()


def test_merge_pdfs_empty_list(tmp_path):
    from src.core.organizer import merge_pdfs
    with pytest.raises(ValueError):
        merge_pdfs([], str(tmp_path / "out.pdf"))


def test_merge_pdfs_file_not_found(tmp_path):
    from src.core.organizer import merge_pdfs
    pdf = _make_pdf(tmp_path)
    with pytest.raises(FileNotFoundError):
        merge_pdfs([pdf, "/nonexistent.pdf"], str(tmp_path / "out.pdf"))


# ---------------------------------------------------------------------------
# split_pdf_into_pages
# ---------------------------------------------------------------------------

def test_split_into_pages(tmp_path):
    from src.core.organizer import split_pdf_into_pages
    pdf = _make_pdf(tmp_path, pages=3)
    out_dir = str(tmp_path / "split")
    results = split_pdf_into_pages(pdf, out_dir)
    assert len(results) == 3
    for p in results:
        assert os.path.isfile(p)
        doc = fitz.open(p)
        assert doc.page_count == 1
        doc.close()


def test_split_into_pages_file_not_found(tmp_path):
    from src.core.organizer import split_pdf_into_pages
    with pytest.raises(FileNotFoundError):
        split_pdf_into_pages("/nope.pdf", str(tmp_path / "out"))


# ---------------------------------------------------------------------------
# split_pdf_by_ranges
# ---------------------------------------------------------------------------

def test_split_by_ranges(tmp_path):
    from src.core.organizer import split_pdf_by_ranges
    pdf = _make_pdf(tmp_path, pages=5)
    out_dir = str(tmp_path / "split")
    results = split_pdf_by_ranges(pdf, [(1, 2), (3, 5)], out_dir)
    assert len(results) == 2
    doc0 = fitz.open(results[0])
    assert doc0.page_count == 2
    doc0.close()
    doc1 = fitz.open(results[1])
    assert doc1.page_count == 3
    doc1.close()


# ---------------------------------------------------------------------------
# rotate_pages
# ---------------------------------------------------------------------------

def test_rotate_pages_all(tmp_path):
    from src.core.organizer import rotate_pages
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "rotated.pdf")
    result = rotate_pages(pdf, out, [], 90)
    assert os.path.isfile(result)
    doc = fitz.open(result)
    for page in doc:
        assert page.rotation in (90, 270)  # original 0 + 90
    doc.close()


def test_rotate_pages_selected(tmp_path):
    from src.core.organizer import rotate_pages
    pdf = _make_pdf(tmp_path, pages=3)
    out = str(tmp_path / "rotated.pdf")
    rotate_pages(pdf, out, [0, 2], 180)
    assert os.path.isfile(out)


# ---------------------------------------------------------------------------
# crop_pages
# ---------------------------------------------------------------------------

def test_crop_pages(tmp_path):
    from src.core.organizer import crop_pages
    pdf = _make_pdf(tmp_path, pages=2)
    out = str(tmp_path / "cropped.pdf")
    result = crop_pages(pdf, out, [], {"left": 10, "right": 10, "top": 10, "bottom": 10})
    assert os.path.isfile(result)


# ---------------------------------------------------------------------------
# reorder_pages
# ---------------------------------------------------------------------------

def test_reorder_pages(tmp_path):
    from src.core.organizer import reorder_pages
    pdf = _make_pdf(tmp_path, pages=3)
    out = str(tmp_path / "reordered.pdf")
    result = reorder_pages(pdf, out, [2, 0, 1])
    doc = fitz.open(result)
    assert doc.page_count == 3
    doc.close()
