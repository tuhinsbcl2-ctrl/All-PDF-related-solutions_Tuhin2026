"""
PDF compression operations.
Supports low / medium / high compression levels.
"""

import os
import fitz  # PyMuPDF


COMPRESSION_LEVELS = {
    "low": {"image_quality": 85, "deflate": True, "garbage": 1},
    "medium": {"image_quality": 60, "deflate": True, "garbage": 3},
    "high": {"image_quality": 35, "deflate": True, "garbage": 4},
}


def compress_pdf(
    pdf_path: str,
    output_path: str,
    level: str = "medium",
) -> dict:
    """
    Compress a PDF file.

    level: 'low' | 'medium' | 'high'
    Returns a dict with before/after sizes and compression ratio.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    level = level.lower()
    if level not in COMPRESSION_LEVELS:
        raise ValueError(f"Invalid level '{level}'. Choose from: {list(COMPRESSION_LEVELS.keys())}")

    opts = COMPRESSION_LEVELS[level]
    size_before = os.path.getsize(pdf_path)

    doc = fitz.open(pdf_path)
    doc.save(
        output_path,
        garbage=opts["garbage"],
        deflate=opts["deflate"],
        deflate_images=True,
        deflate_fonts=True,
        clean=True,
    )
    doc.close()

    size_after = os.path.getsize(output_path)
    ratio = (1 - size_after / size_before) * 100 if size_before > 0 else 0

    return {
        "size_before": size_before,
        "size_after": size_after,
        "ratio": round(ratio, 2),
        "output_path": output_path,
    }
