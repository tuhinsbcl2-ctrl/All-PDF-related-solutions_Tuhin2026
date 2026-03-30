"""
Tests for core/security.py
"""

import os
import pytest
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
import pikepdf


def _make_pdf(tmp_path: Path) -> str:
    path = str(tmp_path / "test.pdf")
    c = rl_canvas.Canvas(path)
    c.drawString(72, 700, "Secure document")
    c.save()
    return path


# ---------------------------------------------------------------------------
# lock_pdf
# ---------------------------------------------------------------------------

def test_lock_pdf_creates_encrypted_file(tmp_path):
    from src.core.security import lock_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "locked.pdf")
    result = lock_pdf(pdf, out, user_password="secret")
    assert result == out
    assert os.path.isfile(out)
    # Verify it is actually encrypted
    with pikepdf.open(out, password="secret") as p:
        assert len(p.pages) >= 1


def test_lock_pdf_with_owner_password(tmp_path):
    from src.core.security import lock_pdf
    pdf = _make_pdf(tmp_path)
    out = str(tmp_path / "locked.pdf")
    lock_pdf(pdf, out, user_password="user", owner_password="owner")
    assert os.path.isfile(out)


def test_lock_pdf_file_not_found(tmp_path):
    from src.core.security import lock_pdf
    with pytest.raises(FileNotFoundError):
        lock_pdf("/nonexistent.pdf", str(tmp_path / "out.pdf"), "pw")


# ---------------------------------------------------------------------------
# unlock_pdf
# ---------------------------------------------------------------------------

def test_unlock_pdf(tmp_path):
    from src.core.security import lock_pdf, unlock_pdf
    pdf = _make_pdf(tmp_path)
    locked = str(tmp_path / "locked.pdf")
    unlocked = str(tmp_path / "unlocked.pdf")
    lock_pdf(pdf, locked, user_password="secret")
    result = unlock_pdf(locked, unlocked, password="secret")
    assert result == unlocked
    assert os.path.isfile(unlocked)
    # Should open without password
    with pikepdf.open(unlocked) as p:
        assert len(p.pages) >= 1


def test_unlock_pdf_wrong_password(tmp_path):
    from src.core.security import lock_pdf, unlock_pdf
    pdf = _make_pdf(tmp_path)
    locked = str(tmp_path / "locked.pdf")
    lock_pdf(pdf, locked, user_password="correct")
    with pytest.raises(pikepdf.PasswordError):
        unlock_pdf(locked, str(tmp_path / "out.pdf"), password="wrong")


def test_unlock_pdf_file_not_found(tmp_path):
    from src.core.security import unlock_pdf
    with pytest.raises(FileNotFoundError):
        unlock_pdf("/nonexistent.pdf", str(tmp_path / "out.pdf"), "pw")
