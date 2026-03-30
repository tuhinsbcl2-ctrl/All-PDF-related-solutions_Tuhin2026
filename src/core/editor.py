"""
PDF editing operations:
  - Add/edit text on pages
  - Reorder, add, remove pages
  - Insert images on pages
  - Add signature images on pages
"""

import os
import fitz  # PyMuPDF


def add_text_to_page(
    pdf_path: str,
    output_path: str,
    page_index: int,
    text: str,
    x: float,
    y: float,
    font_size: float = 12,
    color: tuple = (0, 0, 0),
) -> str:
    """
    Add text to a specific page of a PDF at position (x, y).

    color is an (R, G, B) tuple with values 0-1.
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    if page_index < 0 or page_index >= len(doc):
        doc.close()
        raise IndexError(f"Page index {page_index} out of range.")

    page = doc[page_index]
    page.insert_text(
        (x, y),
        text,
        fontsize=font_size,
        color=color,
    )
    doc.save(output_path)
    doc.close()
    return output_path


def remove_pages(pdf_path: str, output_path: str, page_indices: list) -> str:
    """
    Remove pages at the given (0-based) indices from a PDF.

    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    # Delete in reverse order to avoid index shifting
    for idx in sorted(set(page_indices), reverse=True):
        if 0 <= idx < len(doc):
            doc.delete_page(idx)
    doc.save(output_path)
    doc.close()
    return output_path


def add_blank_page(
    pdf_path: str,
    output_path: str,
    insert_after: int = -1,
    width: float = 595,
    height: float = 842,
) -> str:
    """
    Insert a blank page after `insert_after` (0-based index).
    Use -1 to append at the end.

    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    position = insert_after + 1 if insert_after >= 0 else len(doc)
    doc.insert_page(position, width=width, height=height)
    doc.save(output_path)
    doc.close()
    return output_path


def reorder_pages(pdf_path: str, output_path: str, new_order: list) -> str:
    """
    Reorder pages according to `new_order` (list of 0-based page indices).

    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    doc.select(new_order)
    doc.save(output_path)
    doc.close()
    return output_path


def insert_image_on_page(
    pdf_path: str,
    output_path: str,
    page_index: int,
    image_path: str,
    rect: tuple,
) -> str:
    """
    Insert an image onto a PDF page at the given rectangle.

    rect: (x0, y0, x1, y1) in points.
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    doc = fitz.open(pdf_path)
    if page_index < 0 or page_index >= len(doc):
        doc.close()
        raise IndexError(f"Page index {page_index} out of range.")

    page = doc[page_index]
    page.insert_image(fitz.Rect(*rect), filename=image_path)
    doc.save(output_path)
    doc.close()
    return output_path


def add_signature(
    pdf_path: str,
    output_path: str,
    page_index: int,
    signature_image_path: str,
    rect: tuple,
) -> str:
    """
    Place a signature image on a specific page at the given rectangle.

    This is an alias for insert_image_on_page with signature semantics.
    rect: (x0, y0, x1, y1) in points.
    Returns output path.
    """
    return insert_image_on_page(
        pdf_path, output_path, page_index, signature_image_path, rect
    )
