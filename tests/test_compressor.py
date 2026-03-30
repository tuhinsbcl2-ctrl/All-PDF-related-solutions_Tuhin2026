"""
Tests for core/compressor.py
"""

import os
import pytest
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas


def _make_pdf(tmp_path: Path, pages: int = 2) -> str:
    path = str(tmp_path / "test.pdf")
    c = rl_canvas.Canvas(path)
    for i in range(pages):
        c.drawString(72, 700, f"Page {i + 1} content with some text to compress.")
        c.showPage()
    c.save()
    return path


def test_compress_low(tmp_path):
    from src.core.compressor import compress_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "compressed.pdf")
    result = compress_pdf(pdf, out, level="low")
    assert os.path.isfile(out)
    assert result["size_before"] > 0
    assert result["size_after"] > 0
    assert "ratio" in result
    assert result["output_path"] == out


def test_compress_medium(tmp_path):
    from src.core.compressor import compress_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "compressed.pdf")
    result = compress_pdf(pdf, out, level="medium")
    assert os.path.isfile(out)


def test_compress_high(tmp_path):
    from src.core.compressor import compress_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "compressed.pdf")
    result = compress_pdf(pdf, out, level="high")
    assert os.path.isfile(out)


def test_compress_invalid_level(tmp_path):
    from src.core.compressor import compress_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "compressed.pdf")
    with pytest.raises(ValueError):
        compress_pdf(pdf, out, level="ultra")


def test_compress_file_not_found(tmp_path):
    from src.core.compressor import compress_pdf
    with pytest.raises(FileNotFoundError):
        compress_pdf("/nonexistent.pdf", str(tmp_path / "out.pdf"))


def test_compress_result_has_size_fields(tmp_path):
    from src.core.compressor import compress_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "compressed.pdf")
    result = compress_pdf(pdf, out)
    assert "size_before" in result
    assert "size_after" in result
    assert isinstance(result["ratio"], float)
