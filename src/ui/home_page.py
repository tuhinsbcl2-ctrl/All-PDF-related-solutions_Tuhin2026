"""
Home/dashboard page with feature cards.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


FEATURES = [
    # (page_key, icon, title, description, category_color)
    ("pdf_to_excel",  "📊", "PDF to Excel",    "Extract tables from PDF to .xlsx",           "#4CAF50"),
    ("excel_to_pdf",  "📄", "Excel to PDF",    "Convert .xlsx spreadsheets to PDF",          "#4CAF50"),
    ("pdf_to_word",   "📝", "PDF to Word",     "Extract PDF text to .docx format",           "#2196F3"),
    ("word_to_pdf",   "📝", "Word to PDF",     "Convert .docx documents to PDF",             "#2196F3"),
    ("photos_to_pdf", "🖼️", "Photos to PDF",  "Combine images into a single PDF",           "#9C27B0"),
    ("pdf_to_photos", "📸", "PDF to Photos",  "Export PDF pages as PNG/JPG images",         "#9C27B0"),
    ("compress",      "🗜️", "Compress PDF",   "Reduce PDF file size",                        "#FF9800"),
    ("editor",        "✏️", "PDF Editor",     "Add text, images & signatures to PDF",       "#F44336"),
    ("lock_unlock",   "🔐", "Lock / Unlock",  "Password-protect or decrypt PDFs",           "#607D8B"),
    ("page_numbers",  "🔢", "Page Numbers",   "Add page numbers to your PDF",               "#00BCD4"),
    ("merge",         "🔗", "Merge PDFs",     "Combine multiple PDFs into one",             "#3F51B5"),
    ("split",         "✂️", "Split PDF",      "Split a PDF into parts or pages",            "#3F51B5"),
    ("rotate",        "🔄", "Rotate Pages",   "Rotate selected or all PDF pages",           "#795548"),
    ("crop",          "⬛", "Crop PDF",        "Crop page margins",                          "#795548"),
    ("repair",        "🔧", "Repair PDF",     "Attempt to fix corrupted PDF files",         "#FF5722"),
    ("organize",      "📋", "Organize Pages", "Reorder or delete PDF pages visually",       "#009688"),
    ("watermark",     "💧", "Watermark",      "Add or remove text/image watermarks",        "#673AB7"),
]


class FeatureCard(QFrame):
    """Clickable card for a single feature."""

    clicked = Signal(str)  # emits page_key

    def __init__(self, page_key: str, icon: str, title: str, description: str, color: str, parent=None):
        super().__init__(parent)
        self._page_key = page_key
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedSize(180, 140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            FeatureCard {{
                background-color: #24273A;
                border-radius: 10px;
                border: 1px solid #313244;
            }}
            FeatureCard:hover {{
                border: 1px solid {color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)

        icon_lbl = QLabel(icon, self)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 28px; background: transparent;")
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(title, self)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {color}; background: transparent;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel(description, self)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 11px; color: #A6ADC8; background: transparent;")
        layout.addWidget(desc_lbl)

    def mousePressEvent(self, event):
        self.clicked.emit(self._page_key)
        super().mousePressEvent(event)


class HomePage(QWidget):
    """Dashboard page displaying all feature cards."""

    feature_selected = Signal(str)  # emits page_key

    def __init__(self, parent=None):
        super().__init__(parent)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(16)

        # Header
        title = QLabel("PDF Solutions", self)
        title.setObjectName("titleLabel")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        outer_layout.addWidget(title)

        subtitle = QLabel("All-in-one desktop toolkit for PDF operations", self)
        subtitle.setObjectName("subtitleLabel")
        outer_layout.addWidget(subtitle)

        # Scroll area for cards
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(16)
        grid.setContentsMargins(0, 16, 0, 16)

        cols = 5
        for i, (page_key, icon, title_txt, desc, color) in enumerate(FEATURES):
            card = FeatureCard(page_key, icon, title_txt, desc, color)
            card.clicked.connect(self.feature_selected.emit)
            grid.addWidget(card, i // cols, i % cols)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll, stretch=1)
