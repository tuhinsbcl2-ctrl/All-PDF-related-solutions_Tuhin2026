"""
Common PDF utility functions.
"""

import fitz  # PyMuPDF


def get_page_count(pdf_path: str) -> int:
    """Return the number of pages in a PDF."""
    with fitz.open(pdf_path) as doc:
        return doc.page_count


def get_pdf_metadata(pdf_path: str) -> dict:
    """Return metadata dict for a PDF."""
    with fitz.open(pdf_path) as doc:
        return doc.metadata


def is_pdf_encrypted(pdf_path: str) -> bool:
    """Return True if the PDF is encrypted/password-protected."""
    with fitz.open(pdf_path) as doc:
        return doc.is_encrypted


def render_page_to_pixmap(pdf_path: str, page_index: int, dpi: int = 150):
    """
    Render a single PDF page to a PyMuPDF Pixmap.

    Returns a fitz.Pixmap object.
    """
    with fitz.open(pdf_path) as doc:
        page = doc[page_index]
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        return page.get_pixmap(matrix=mat, alpha=False)


def extract_text_from_page(pdf_path: str, page_index: int) -> str:
    """Extract plain text from a single page."""
    with fitz.open(pdf_path) as doc:
        return doc[page_index].get_text()


def extract_all_text(pdf_path: str) -> list[str]:
    """Extract text from every page; returns list of strings (one per page)."""
    with fitz.open(pdf_path) as doc:
        return [page.get_text() for page in doc]
