"""
Add page numbers to PDF pages.
"""

import os
import fitz  # PyMuPDF


POSITIONS = {
    # (x_fraction, y_fraction, align)  – fractions of page width/height
    "bottom-center": (0.5, 0.95, "center"),
    "bottom-left": (0.05, 0.95, "left"),
    "bottom-right": (0.95, 0.95, "right"),
    "top-center": (0.5, 0.05, "center"),
    "top-left": (0.05, 0.05, "left"),
    "top-right": (0.95, 0.05, "right"),
}

# Approximate character width as a fraction of font size (used for alignment)
_CHAR_WIDTH_FACTOR = 0.5


def add_page_numbers(
    pdf_path: str,
    output_path: str,
    position: str = "bottom-center",
    font_size: float = 12,
    start_number: int = 1,
    color: tuple = (0, 0, 0),
    prefix: str = "",
    suffix: str = "",
) -> str:
    """
    Add page numbers to all pages of a PDF.

    position    – one of the keys in POSITIONS.
    font_size   – size in points.
    start_number– the number printed on the first page.
    prefix/suffix – optional strings around the number, e.g. "Page " / " of N".
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pos_key = position.lower().replace(" ", "-")
    if pos_key not in POSITIONS:
        raise ValueError(
            f"Invalid position '{position}'. Choose from: {list(POSITIONS.keys())}"
        )

    x_frac, y_frac, align = POSITIONS[pos_key]
    doc = fitz.open(pdf_path)
    total = len(doc)

    for i, page in enumerate(doc):
        number = start_number + i
        label = f"{prefix}{number}{suffix}"
        rect = page.rect
        x = rect.width * x_frac
        y = rect.height * y_frac

        if align == "center":
            # Estimate text width to centre it
            char_w = font_size * _CHAR_WIDTH_FACTOR
            x -= len(label) * char_w / 2
        elif align == "right":
            char_w = font_size * _CHAR_WIDTH_FACTOR
            x -= len(label) * char_w

        page.insert_text(
            (x, y),
            label,
            fontsize=font_size,
            color=color,
        )

    doc.save(output_path)
    doc.close()
    return output_path
