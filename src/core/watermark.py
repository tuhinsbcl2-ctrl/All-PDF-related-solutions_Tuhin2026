"""
Watermark operations: add and remove watermarks from PDFs.
"""

import os
import fitz  # PyMuPDF


# Approximate text width as a fraction of font size (used for centering)
_TEXT_WIDTH_FACTOR = 0.3


    pdf_path: str,
    output_path: str,
    text: str,
    font_size: float = 48,
    opacity: float = 0.3,
    angle: float = 45,
    color: tuple = (0.5, 0.5, 0.5),
    page_indices: list = None,
) -> str:
    """
    Add a text watermark to each (or selected) pages of a PDF.

    page_indices – 0-based list; pass None to watermark all pages.
    opacity      – 0.0 (transparent) to 1.0 (opaque).
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    indices = page_indices if page_indices is not None else list(range(len(doc)))

    for idx in indices:
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = page.rect
            # Place watermark at page center
            x = rect.width / 2
            y = rect.height / 2
            page.insert_text(
                (x - len(text) * font_size * _TEXT_WIDTH_FACTOR, y),
                text,
                fontsize=font_size,
                color=color,
                rotate=angle,
                overlay=True,
            )

    doc.save(output_path)
    doc.close()
    return output_path


def add_image_watermark(
    pdf_path: str,
    output_path: str,
    image_path: str,
    opacity: float = 0.3,
    page_indices: list = None,
) -> str:
    """
    Add an image watermark to each (or selected) pages of a PDF.

    page_indices – 0-based list; pass None to watermark all pages.
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    doc = fitz.open(pdf_path)
    indices = page_indices if page_indices is not None else list(range(len(doc)))

    for idx in indices:
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = page.rect
            # Centre the image and use 50% of page width
            img_w = rect.width * 0.5
            img_h = rect.height * 0.5
            x0 = (rect.width - img_w) / 2
            y0 = (rect.height - img_h) / 2
            img_rect = fitz.Rect(x0, y0, x0 + img_w, y0 + img_h)
            page.insert_image(img_rect, filename=image_path, overlay=True)

    doc.save(output_path)
    doc.close()
    return output_path


def remove_watermark_text(
    pdf_path: str,
    output_path: str,
    watermark_text: str,
) -> str:
    """
    Attempt to remove text watermark by redacting occurrences of `watermark_text`.

    Note: This works for watermarks added as searchable text.
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    for page in doc:
        rects = page.search_for(watermark_text)
        for rect in rects:
            page.add_redact_annot(rect)
        page.apply_redactions()

    doc.save(output_path)
    doc.close()
    return output_path
