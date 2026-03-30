"""
PDF preview widget – renders PDF pages as thumbnails using PyMuPDF.
"""

import fitz
from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap


class PreviewWidget(QWidget):
    """
    Displays a rendered preview of a single PDF page.

    Signals:
        page_changed(int): emitted when the user navigates to a new page.
    """

    page_changed = Signal(int)
    PREVIEW_ZOOM = 1.5  # Zoom factor for page rendering (higher = sharper but slower)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf_path = None
        self._page_index = 0
        self._page_count = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Scroll area for the image
        self._scroll = QScrollArea(self)
        self._scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._scroll.setWidgetResizable(True)
        self._image_label = QLabel(self)
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setText("No PDF loaded")
        self._image_label.setStyleSheet("color: #6C7086;")
        self._scroll.setWidget(self._image_label)
        layout.addWidget(self._scroll, stretch=1)

        # Navigation bar
        nav_layout = QHBoxLayout()
        self._prev_btn = QPushButton("◀ Prev")
        self._prev_btn.setObjectName("secondaryBtn")
        self._prev_btn.setEnabled(False)
        self._prev_btn.clicked.connect(self._prev_page)
        nav_layout.addWidget(self._prev_btn)

        self._page_label = QLabel("", self)
        self._page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self._page_label, stretch=1)

        self._next_btn = QPushButton("Next ▶")
        self._next_btn.setObjectName("secondaryBtn")
        self._next_btn.setEnabled(False)
        self._next_btn.clicked.connect(self._next_page)
        nav_layout.addWidget(self._next_btn)
        layout.addLayout(nav_layout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_pdf(self, pdf_path: str, page_index: int = 0) -> None:
        """Load and display a PDF, starting at `page_index`."""
        self._pdf_path = pdf_path
        try:
            doc = fitz.open(pdf_path)
            self._page_count = doc.page_count
            doc.close()
        except Exception:
            self._page_count = 0

        self._page_index = max(0, min(page_index, self._page_count - 1))
        self._render()

    def clear(self) -> None:
        """Clear the preview."""
        self._pdf_path = None
        self._page_count = 0
        self._page_index = 0
        self._image_label.setText("No PDF loaded")
        self._image_label.setPixmap(QPixmap())
        self._update_nav()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _render(self) -> None:
        if not self._pdf_path or self._page_count == 0:
            self._image_label.setText("No PDF loaded")
            self._update_nav()
            return

        try:
            doc = fitz.open(self._pdf_path)
            page = doc[self._page_index]
            zoom = self.PREVIEW_ZOOM
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            doc.close()

            img = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888,
            )
            self._image_label.setPixmap(QPixmap.fromImage(img))
        except Exception as exc:
            self._image_label.setText(f"Preview error: {exc}")

        self._update_nav()

    def _update_nav(self) -> None:
        self._page_label.setText(
            f"Page {self._page_index + 1} of {self._page_count}"
            if self._page_count > 0
            else ""
        )
        self._prev_btn.setEnabled(self._page_index > 0)
        self._next_btn.setEnabled(self._page_index < self._page_count - 1)

    def _prev_page(self) -> None:
        if self._page_index > 0:
            self._page_index -= 1
            self._render()
            self.page_changed.emit(self._page_index)

    def _next_page(self) -> None:
        if self._page_index < self._page_count - 1:
            self._page_index += 1
            self._render()
            self.page_changed.emit(self._page_index)
