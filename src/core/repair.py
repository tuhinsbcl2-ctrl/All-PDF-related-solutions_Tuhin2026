"""
PDF repair operations.
Attempts to rebuild the PDF structure using PyMuPDF.
"""

import os
import fitz  # PyMuPDF


def repair_pdf(pdf_path: str, output_path: str) -> dict:
    """
    Attempt to repair a potentially corrupted PDF.

    Opens the file with error recovery enabled, then saves it cleanly.
    Returns a dict with 'success', 'output_path', and 'message'.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        # fitz.open with filetype hint helps with corrupted files
        doc = fitz.open(pdf_path)
        page_count = doc.page_count

        doc.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True,
        )
        doc.close()

        return {
            "success": True,
            "output_path": output_path,
            "page_count": page_count,
            "message": f"Repaired successfully. {page_count} page(s) recovered.",
        }
    except Exception as exc:
        return {
            "success": False,
            "output_path": None,
            "page_count": 0,
            "message": f"Repair failed: {exc}",
        }
