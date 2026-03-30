"""
PDF organizer operations:
  - Merge multiple PDFs
  - Split PDF
  - Rotate pages
  - Crop pages
  - Reorder pages
"""

import os
import fitz  # PyMuPDF
from pypdf import PdfWriter, PdfReader


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge_pdfs(pdf_paths: list, output_path: str) -> str:
    """
    Merge multiple PDF files into one.

    pdf_paths – ordered list of input PDF file paths.
    Returns output path.
    """
    if not pdf_paths:
        raise ValueError("No PDF paths provided.")

    writer = PdfWriter()
    for path in pdf_paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"PDF not found: {path}")
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

def split_pdf_by_ranges(pdf_path: str, ranges: list, output_dir: str) -> list:
    """
    Split a PDF by page ranges.

    ranges – list of (start, end) tuples (1-based, inclusive).
    Returns list of output file paths.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(pdf_path)
    output_paths = []
    stem = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, (start, end) in enumerate(ranges, 1):
        writer = PdfWriter()
        for page_num in range(start - 1, min(end, len(reader.pages))):
            writer.add_page(reader.pages[page_num])
        out_file = os.path.join(output_dir, f"{stem}_part{i}.pdf")
        with open(out_file, "wb") as f:
            writer.write(f)
        output_paths.append(out_file)

    return output_paths


def split_pdf_into_pages(pdf_path: str, output_dir: str) -> list:
    """
    Split each page of a PDF into its own file.

    Returns list of output file paths.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(pdf_path)
    output_paths = []
    stem = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        out_file = os.path.join(output_dir, f"{stem}_page{i}.pdf")
        with open(out_file, "wb") as f:
            writer.write(f)
        output_paths.append(out_file)

    return output_paths


# ---------------------------------------------------------------------------
# Rotate
# ---------------------------------------------------------------------------

def rotate_pages(
    pdf_path: str,
    output_path: str,
    page_indices: list,
    angle: int,
) -> str:
    """
    Rotate selected pages by `angle` degrees (90, 180, 270).

    page_indices – 0-based list; pass None or empty list to rotate all pages.
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    indices = page_indices if page_indices else list(range(len(doc)))

    for idx in indices:
        if 0 <= idx < len(doc):
            page = doc[idx]
            page.set_rotation((page.rotation + angle) % 360)

    doc.save(output_path)
    doc.close()
    return output_path


# ---------------------------------------------------------------------------
# Crop
# ---------------------------------------------------------------------------

def crop_pages(
    pdf_path: str,
    output_path: str,
    page_indices: list,
    margins: dict,
) -> str:
    """
    Crop pages by adjusting their media box.

    page_indices – 0-based list; pass None or empty list to crop all pages.
    margins – dict with keys 'left', 'right', 'top', 'bottom' (in points).
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    left = margins.get("left", 0)
    right = margins.get("right", 0)
    top = margins.get("top", 0)
    bottom = margins.get("bottom", 0)

    doc = fitz.open(pdf_path)
    indices = page_indices if page_indices else list(range(len(doc)))

    for idx in indices:
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = page.rect
            new_rect = fitz.Rect(
                rect.x0 + left,
                rect.y0 + top,
                rect.x1 - right,
                rect.y1 - bottom,
            )
            page.set_cropbox(new_rect)

    doc.save(output_path)
    doc.close()
    return output_path


# ---------------------------------------------------------------------------
# Reorder / Organize
# ---------------------------------------------------------------------------

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
