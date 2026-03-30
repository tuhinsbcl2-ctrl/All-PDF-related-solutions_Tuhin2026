"""
Main window with sidebar navigation and all feature pages.
"""

import os
import traceback
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QSizePolicy,
    QFrame,
    QTextEdit,
    QSplitter,
    QSlider,
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QFont

from src.ui.widgets.file_drop_widget import FileDropWidget
from src.ui.widgets.progress_widget import ProgressWidget
from src.ui.widgets.preview_widget import PreviewWidget
from src.ui.home_page import HomePage
from src.ui.styles import get_theme


# ---------------------------------------------------------------------------
# Worker thread base
# ---------------------------------------------------------------------------

class WorkerSignals(QObject):
    finished = Signal(object)   # result object
    error = Signal(str)         # error message
    progress = Signal(int, str) # value, message


class Worker(QThread):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self._fn(*self._args, **self._kwargs)
            self.signals.finished.emit(result)
        except Exception as exc:
            self.signals.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Base feature page
# ---------------------------------------------------------------------------

class BaseFeaturePage(QWidget):
    """
    Template for a feature page:
    ┌──────────────────────────────────────────┐
    │ Title / description                       │
    │ FileDropWidget                            │
    │ Options group                             │
    │ [Process button]  [Progress]             │
    └──────────────────────────────────────────┘
    """

    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self._worker = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(16)

        # Header
        title_lbl = QLabel(title, self)
        title_lbl.setObjectName("titleLabel")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        outer.addWidget(title_lbl)

        sub_lbl = QLabel(subtitle, self)
        sub_lbl.setObjectName("subtitleLabel")
        outer.addWidget(sub_lbl)

        # Scroll content
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content_widget = QWidget()
        self._content_layout = QVBoxLayout(content_widget)
        self._content_layout.setSpacing(16)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(content_widget)
        outer.addWidget(scroll, stretch=1)

        # Progress bar (added last inside content)
        self._progress = ProgressWidget(self)
        self._content_layout.addWidget(self._progress)
        self._content_layout.addStretch()

    def _add_to_content(self, widget: QWidget, stretch: int = 0) -> None:
        """Insert widget before the stretch at the end."""
        count = self._content_layout.count()
        self._content_layout.insertWidget(count - 2, widget, stretch)

    def _show_success(self, message: str) -> None:
        self._progress.finish("✅ " + message)
        QMessageBox.information(self, "Success", message)

    def _show_error(self, message: str) -> None:
        self._progress.reset()
        QMessageBox.critical(self, "Error", message)

    def _run_worker(self, fn, *args, start_msg="Processing…", **kwargs) -> None:
        self._progress.start(start_msg)
        self._worker = Worker(fn, *args, **kwargs)
        self._worker.signals.finished.connect(self._on_worker_finished)
        self._worker.signals.error.connect(self._on_worker_error)
        self._worker.start()

    def _on_worker_finished(self, result) -> None:
        self._progress.finish("✅ Done!")

    def _on_worker_error(self, error: str) -> None:
        self._show_error(error)

    @staticmethod
    def _save_dialog(parent, title: str, ext_filter: str, default_name: str = "") -> str:
        path, _ = QFileDialog.getSaveFileName(parent, title, default_name, ext_filter)
        return path


# ---------------------------------------------------------------------------
# PDF to Excel page
# ---------------------------------------------------------------------------

class PdfToExcelPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("PDF to Excel", "Extract text/tables from PDF to .xlsx spreadsheet", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        btn = QPushButton("Convert to Excel")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import pdf_to_excel
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Excel File", "Excel Files (*.xlsx)", pdf.replace(".pdf", ".xlsx"))
        if not out:
            return
        self._run_worker(pdf_to_excel, pdf, out, start_msg="Converting PDF to Excel…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Excel to PDF page
# ---------------------------------------------------------------------------

class ExcelToPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Excel to PDF", "Convert .xlsx spreadsheets to a styled PDF", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".xlsx", ".xls"], multiple=False,
                                         label_text="Drop Excel file here or click Browse")
        self._add_to_content(self._file_drop)

        btn = QPushButton("Convert to PDF")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import excel_to_pdf
        xlsx = self._file_drop.file
        if not xlsx:
            return self._show_error("Please select an Excel file.")
        out = self._save_dialog(self, "Save PDF File", "PDF Files (*.pdf)", xlsx.replace(".xlsx", ".pdf"))
        if not out:
            return
        self._run_worker(excel_to_pdf, xlsx, out, start_msg="Converting Excel to PDF…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# PDF to Word page
# ---------------------------------------------------------------------------

class PdfToWordPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("PDF to Word", "Extract text from PDF and save as .docx", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        btn = QPushButton("Convert to Word")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import pdf_to_word
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Word File", "Word Files (*.docx)", pdf.replace(".pdf", ".docx"))
        if not out:
            return
        self._run_worker(pdf_to_word, pdf, out, start_msg="Converting PDF to Word…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Word to PDF page
# ---------------------------------------------------------------------------

class WordToPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Word to PDF", "Convert .docx documents to PDF", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".docx", ".doc"], multiple=False,
                                         label_text="Drop Word document here or click Browse")
        self._add_to_content(self._file_drop)

        btn = QPushButton("Convert to PDF")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import word_to_pdf
        docx = self._file_drop.file
        if not docx:
            return self._show_error("Please select a Word document.")
        out = self._save_dialog(self, "Save PDF File", "PDF Files (*.pdf)", docx.replace(".docx", ".pdf"))
        if not out:
            return
        self._run_worker(word_to_pdf, docx, out, start_msg="Converting Word to PDF…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Photos to PDF page
# ---------------------------------------------------------------------------

class PhotosToPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Photos to PDF", "Combine multiple images into a single PDF", parent)

        self._file_drop = FileDropWidget(
            accept_extensions=[".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"],
            multiple=True,
            label_text="Drop images here or click Browse (multiple allowed)",
        )
        self._add_to_content(self._file_drop)

        btn = QPushButton("Convert to PDF")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import photos_to_pdf
        images = self._file_drop.files
        if not images:
            return self._show_error("Please select at least one image file.")
        out = self._save_dialog(self, "Save PDF File", "PDF Files (*.pdf)", "output.pdf")
        if not out:
            return
        self._run_worker(photos_to_pdf, images, out, start_msg="Converting images to PDF…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# PDF to Photos page
# ---------------------------------------------------------------------------

class PdfToPhotosPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("PDF to Photos", "Export PDF pages as PNG/JPG images", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Options")
        form = QFormLayout(opts)
        self._dpi_spin = QSpinBox()
        self._dpi_spin.setRange(72, 600)
        self._dpi_spin.setValue(150)
        form.addRow("DPI:", self._dpi_spin)

        self._fmt_combo = QComboBox()
        self._fmt_combo.addItems(["PNG", "JPEG"])
        form.addRow("Format:", self._fmt_combo)
        self._add_to_content(opts)

        btn = QPushButton("Export Pages as Images")
        btn.clicked.connect(self._convert)
        self._add_to_content(btn)

    def _convert(self):
        from src.core.converter import pdf_to_photos
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not out_dir:
            return
        dpi = self._dpi_spin.value()
        fmt = self._fmt_combo.currentText()
        self._run_worker(pdf_to_photos, pdf, out_dir, dpi, fmt, start_msg="Exporting pages…")

    def _on_worker_finished(self, result):
        self._show_success(f"Exported {len(result)} image(s) to folder.")


# ---------------------------------------------------------------------------
# Compress PDF page
# ---------------------------------------------------------------------------

class CompressPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Compress PDF", "Reduce PDF file size while preserving quality", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Compression Options")
        form = QFormLayout(opts)
        self._level_combo = QComboBox()
        self._level_combo.addItems(["low", "medium", "high"])
        self._level_combo.setCurrentIndex(1)
        form.addRow("Level:", self._level_combo)
        self._add_to_content(opts)

        btn = QPushButton("Compress PDF")
        btn.clicked.connect(self._compress)
        self._add_to_content(btn)

        self._result_label = QLabel("")
        self._result_label.setWordWrap(True)
        self._add_to_content(self._result_label)

    def _compress(self):
        from src.core.compressor import compress_pdf
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Compressed PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_compressed.pdf"))
        if not out:
            return
        level = self._level_combo.currentText()
        self._run_worker(compress_pdf, pdf, out, level, start_msg="Compressing…")

    def _on_worker_finished(self, result):
        before = result["size_before"] / 1024
        after = result["size_after"] / 1024
        ratio = result["ratio"]
        self._result_label.setText(
            f"✅ Before: {before:.1f} KB  →  After: {after:.1f} KB  (saved {ratio:.1f}%)"
        )
        self._progress.finish("Done!")
        QMessageBox.information(self, "Compressed",
                                f"Before: {before:.1f} KB\nAfter: {after:.1f} KB\nSaved: {ratio:.1f}%\n\nSaved to:\n{result['output_path']}")


# ---------------------------------------------------------------------------
# PDF Editor page
# ---------------------------------------------------------------------------

class PdfEditorPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("PDF Editor", "Add text, images, or signatures to PDF pages", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        # Text options
        text_grp = QGroupBox("Add Text")
        text_form = QFormLayout(text_grp)
        self._text_input = QLineEdit()
        self._text_input.setPlaceholderText("Text to add…")
        text_form.addRow("Text:", self._text_input)
        self._page_spin = QSpinBox()
        self._page_spin.setRange(1, 9999)
        text_form.addRow("Page:", self._page_spin)
        self._x_spin = QDoubleSpinBox()
        self._x_spin.setRange(0, 2000)
        self._x_spin.setValue(72)
        text_form.addRow("X (pts):", self._x_spin)
        self._y_spin = QDoubleSpinBox()
        self._y_spin.setRange(0, 2000)
        self._y_spin.setValue(100)
        text_form.addRow("Y (pts):", self._y_spin)
        self._font_size_spin = QDoubleSpinBox()
        self._font_size_spin.setRange(4, 200)
        self._font_size_spin.setValue(12)
        text_form.addRow("Font size:", self._font_size_spin)
        add_text_btn = QPushButton("Add Text to PDF")
        add_text_btn.clicked.connect(self._add_text)
        text_form.addRow(add_text_btn)
        self._add_to_content(text_grp)

        # Image/Signature options
        img_grp = QGroupBox("Add Image / Signature")
        img_form = QFormLayout(img_grp)
        self._img_drop = FileDropWidget(
            accept_extensions=[".png", ".jpg", ".jpeg", ".bmp"],
            multiple=False,
            label_text="Drop image/signature here",
        )
        img_form.addRow(self._img_drop)
        self._img_page_spin = QSpinBox()
        self._img_page_spin.setRange(1, 9999)
        img_form.addRow("Page:", self._img_page_spin)
        self._img_x0 = QDoubleSpinBox(); self._img_x0.setRange(0, 2000); self._img_x0.setValue(50)
        self._img_y0 = QDoubleSpinBox(); self._img_y0.setRange(0, 2000); self._img_y0.setValue(50)
        self._img_x1 = QDoubleSpinBox(); self._img_x1.setRange(0, 2000); self._img_x1.setValue(200)
        self._img_y1 = QDoubleSpinBox(); self._img_y1.setRange(0, 2000); self._img_y1.setValue(150)
        img_form.addRow("X0:", self._img_x0)
        img_form.addRow("Y0:", self._img_y0)
        img_form.addRow("X1:", self._img_x1)
        img_form.addRow("Y1:", self._img_y1)
        add_img_btn = QPushButton("Add Image to PDF")
        add_img_btn.clicked.connect(self._add_image)
        img_form.addRow(add_img_btn)
        self._add_to_content(img_grp)

        # Remove page
        rm_grp = QGroupBox("Remove Pages")
        rm_form = QFormLayout(rm_grp)
        self._rm_pages_input = QLineEdit()
        self._rm_pages_input.setPlaceholderText("e.g. 1,3,5")
        rm_form.addRow("Page numbers (1-based):", self._rm_pages_input)
        rm_btn = QPushButton("Remove Pages")
        rm_btn.clicked.connect(self._remove_pages)
        rm_form.addRow(rm_btn)
        self._add_to_content(rm_grp)

        # Add blank page
        blank_grp = QGroupBox("Add Blank Page")
        blank_form = QFormLayout(blank_grp)
        self._blank_after_spin = QSpinBox()
        self._blank_after_spin.setRange(0, 9999)
        blank_form.addRow("Insert after page (0=end):", self._blank_after_spin)
        blank_btn = QPushButton("Add Blank Page")
        blank_btn.clicked.connect(self._add_blank)
        blank_form.addRow(blank_btn)
        self._add_to_content(blank_grp)

    def _get_pdf_and_output(self):
        pdf = self._file_drop.file
        if not pdf:
            self._show_error("Please select a PDF file.")
            return None, None
        out = self._save_dialog(self, "Save Edited PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_edited.pdf"))
        return pdf, out

    def _add_text(self):
        from src.core.editor import add_text_to_page
        pdf, out = self._get_pdf_and_output()
        if not out:
            return
        text = self._text_input.text().strip()
        if not text:
            return self._show_error("Please enter text to add.")
        page = self._page_spin.value() - 1
        self._run_worker(
            add_text_to_page, pdf, out, page,
            text, self._x_spin.value(), self._y_spin.value(),
            self._font_size_spin.value(),
            start_msg="Adding text…",
        )

    def _add_image(self):
        from src.core.editor import insert_image_on_page
        pdf, out = self._get_pdf_and_output()
        if not out:
            return
        img = self._img_drop.file
        if not img:
            return self._show_error("Please select an image.")
        page = self._img_page_spin.value() - 1
        rect = (self._img_x0.value(), self._img_y0.value(),
                self._img_x1.value(), self._img_y1.value())
        self._run_worker(insert_image_on_page, pdf, out, page, img, rect, start_msg="Adding image…")

    def _remove_pages(self):
        from src.core.editor import remove_pages
        pdf, out = self._get_pdf_and_output()
        if not out:
            return
        raw = self._rm_pages_input.text().strip()
        try:
            indices = [int(p.strip()) - 1 for p in raw.split(",") if p.strip()]
        except ValueError:
            return self._show_error("Invalid page numbers. Use comma-separated integers.")
        self._run_worker(remove_pages, pdf, out, indices, start_msg="Removing pages…")

    def _add_blank(self):
        from src.core.editor import add_blank_page
        pdf, out = self._get_pdf_and_output()
        if not out:
            return
        after = self._blank_after_spin.value() - 1
        self._run_worker(add_blank_page, pdf, out, after, start_msg="Adding blank page…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Lock/Unlock PDF page
# ---------------------------------------------------------------------------

class LockUnlockPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Lock / Unlock PDF", "Password-protect or decrypt PDF files", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        lock_grp = QGroupBox("Lock PDF (Add Password)")
        lock_form = QFormLayout(lock_grp)
        self._user_pw = QLineEdit(); self._user_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self._user_pw.setPlaceholderText("User password")
        lock_form.addRow("User password:", self._user_pw)
        self._owner_pw = QLineEdit(); self._owner_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self._owner_pw.setPlaceholderText("Owner password (optional)")
        lock_form.addRow("Owner password:", self._owner_pw)
        lock_btn = QPushButton("Lock PDF")
        lock_btn.clicked.connect(self._lock)
        lock_form.addRow(lock_btn)
        self._add_to_content(lock_grp)

        unlock_grp = QGroupBox("Unlock PDF (Remove Password)")
        unlock_form = QFormLayout(unlock_grp)
        self._unlock_pw = QLineEdit(); self._unlock_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self._unlock_pw.setPlaceholderText("Current password")
        unlock_form.addRow("Password:", self._unlock_pw)
        unlock_btn = QPushButton("Unlock PDF")
        unlock_btn.clicked.connect(self._unlock)
        unlock_form.addRow(unlock_btn)
        self._add_to_content(unlock_grp)

    def _lock(self):
        from src.core.security import lock_pdf
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        pw = self._user_pw.text()
        if not pw:
            return self._show_error("Please enter a password.")
        out = self._save_dialog(self, "Save Locked PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_locked.pdf"))
        if not out:
            return
        owner = self._owner_pw.text()
        self._run_worker(lock_pdf, pdf, out, pw, owner, start_msg="Locking PDF…")

    def _unlock(self):
        from src.core.security import unlock_pdf
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        pw = self._unlock_pw.text()
        if not pw:
            return self._show_error("Please enter the current password.")
        out = self._save_dialog(self, "Save Unlocked PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_unlocked.pdf"))
        if not out:
            return
        self._run_worker(unlock_pdf, pdf, out, pw, start_msg="Unlocking PDF…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Page Numbers page
# ---------------------------------------------------------------------------

class PageNumbersPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Add Page Numbers", "Add configurable page numbers to every page", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Options")
        form = QFormLayout(opts)

        self._pos_combo = QComboBox()
        self._pos_combo.addItems([
            "bottom-center", "bottom-left", "bottom-right",
            "top-center", "top-left", "top-right"
        ])
        form.addRow("Position:", self._pos_combo)

        self._start_spin = QSpinBox()
        self._start_spin.setRange(0, 9999)
        self._start_spin.setValue(1)
        form.addRow("Start number:", self._start_spin)

        self._font_size_spin = QDoubleSpinBox()
        self._font_size_spin.setRange(6, 72)
        self._font_size_spin.setValue(12)
        form.addRow("Font size:", self._font_size_spin)

        self._prefix_input = QLineEdit()
        self._prefix_input.setPlaceholderText("e.g. 'Page '")
        form.addRow("Prefix:", self._prefix_input)

        self._suffix_input = QLineEdit()
        self._suffix_input.setPlaceholderText("e.g. ' of 10'")
        form.addRow("Suffix:", self._suffix_input)

        self._add_to_content(opts)

        btn = QPushButton("Add Page Numbers")
        btn.clicked.connect(self._process)
        self._add_to_content(btn)

    def _process(self):
        from src.core.page_numbers import add_page_numbers
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_numbered.pdf"))
        if not out:
            return
        self._run_worker(
            add_page_numbers, pdf, out,
            position=self._pos_combo.currentText(),
            font_size=self._font_size_spin.value(),
            start_number=self._start_spin.value(),
            prefix=self._prefix_input.text(),
            suffix=self._suffix_input.text(),
            start_msg="Adding page numbers…",
        )

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Merge PDFs page
# ---------------------------------------------------------------------------

class MergePdfsPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Merge PDFs", "Combine multiple PDF files into one document", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=True,
                                         label_text="Drop multiple PDFs here or click Browse")
        self._file_drop.files_dropped.connect(self._update_list)
        self._add_to_content(self._file_drop)

        list_grp = QGroupBox("Files to merge (drag to reorder)")
        list_layout = QVBoxLayout(list_grp)
        self._file_list = QListWidget()
        self._file_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._file_list.setMinimumHeight(100)
        list_layout.addWidget(self._file_list)
        self._add_to_content(list_grp)

        btn = QPushButton("Merge PDFs")
        btn.clicked.connect(self._merge)
        self._add_to_content(btn)

    def _update_list(self, files: list) -> None:
        self._file_list.clear()
        for f in files:
            self._file_list.addItem(QListWidgetItem(f))

    def _merge(self):
        from src.core.organizer import merge_pdfs
        # Respect current list order (user may have reordered)
        files = [self._file_list.item(i).text() for i in range(self._file_list.count())]
        if len(files) < 2:
            return self._show_error("Please select at least 2 PDF files.")
        out = self._save_dialog(self, "Save Merged PDF", "PDF Files (*.pdf)", "merged.pdf")
        if not out:
            return
        self._run_worker(merge_pdfs, files, out, start_msg="Merging PDFs…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Split PDF page
# ---------------------------------------------------------------------------

class SplitPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Split PDF", "Split a PDF into individual pages or by ranges", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Split Options")
        form = QFormLayout(opts)

        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["Split into individual pages", "Split by ranges"])
        self._mode_combo.currentIndexChanged.connect(self._toggle_ranges)
        form.addRow("Mode:", self._mode_combo)

        self._ranges_input = QLineEdit()
        self._ranges_input.setPlaceholderText("e.g. 1-3,4-7,8-10")
        self._ranges_input.setEnabled(False)
        form.addRow("Page ranges:", self._ranges_input)
        self._add_to_content(opts)

        btn = QPushButton("Split PDF")
        btn.clicked.connect(self._split)
        self._add_to_content(btn)

    def _toggle_ranges(self, index: int) -> None:
        self._ranges_input.setEnabled(index == 1)

    def _split(self):
        from src.core.organizer import split_pdf_into_pages, split_pdf_by_ranges
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not out_dir:
            return

        if self._mode_combo.currentIndex() == 0:
            self._run_worker(split_pdf_into_pages, pdf, out_dir, start_msg="Splitting…")
        else:
            raw = self._ranges_input.text().strip()
            try:
                ranges = []
                for part in raw.split(","):
                    s, e = part.strip().split("-")
                    ranges.append((int(s), int(e)))
            except Exception:
                return self._show_error("Invalid ranges. Use format: 1-3,4-7")
            self._run_worker(split_pdf_by_ranges, pdf, ranges, out_dir, start_msg="Splitting…")

    def _on_worker_finished(self, result):
        self._show_success(f"Exported {len(result)} file(s) to folder.")


# ---------------------------------------------------------------------------
# Rotate Pages page
# ---------------------------------------------------------------------------

class RotatePagesPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Rotate Pages", "Rotate all or selected pages of a PDF", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Rotation Options")
        form = QFormLayout(opts)

        self._angle_combo = QComboBox()
        self._angle_combo.addItems(["90°", "180°", "270°"])
        form.addRow("Angle:", self._angle_combo)

        self._pages_input = QLineEdit()
        self._pages_input.setPlaceholderText("Leave blank for all pages, or e.g. 1,3,5")
        form.addRow("Pages (1-based):", self._pages_input)
        self._add_to_content(opts)

        btn = QPushButton("Rotate Pages")
        btn.clicked.connect(self._rotate)
        self._add_to_content(btn)

    def _rotate(self):
        from src.core.organizer import rotate_pages
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Rotated PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_rotated.pdf"))
        if not out:
            return
        angle = int(self._angle_combo.currentText().replace("°", ""))
        raw = self._pages_input.text().strip()
        if raw:
            try:
                indices = [int(p.strip()) - 1 for p in raw.split(",") if p.strip()]
            except ValueError:
                return self._show_error("Invalid page numbers.")
        else:
            indices = []
        self._run_worker(rotate_pages, pdf, out, indices, angle, start_msg="Rotating pages…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Crop PDF page
# ---------------------------------------------------------------------------

class CropPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Crop PDF", "Crop page margins for all or selected pages", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        opts = QGroupBox("Crop Margins (in points)")
        form = QFormLayout(opts)
        self._left = QDoubleSpinBox(); self._left.setRange(0, 500)
        self._right = QDoubleSpinBox(); self._right.setRange(0, 500)
        self._top = QDoubleSpinBox(); self._top.setRange(0, 500)
        self._bottom = QDoubleSpinBox(); self._bottom.setRange(0, 500)
        form.addRow("Left:", self._left)
        form.addRow("Right:", self._right)
        form.addRow("Top:", self._top)
        form.addRow("Bottom:", self._bottom)

        self._pages_input = QLineEdit()
        self._pages_input.setPlaceholderText("Leave blank for all pages, or e.g. 1,2,3")
        form.addRow("Pages (1-based):", self._pages_input)
        self._add_to_content(opts)

        btn = QPushButton("Crop PDF")
        btn.clicked.connect(self._crop)
        self._add_to_content(btn)

    def _crop(self):
        from src.core.organizer import crop_pages
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Cropped PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_cropped.pdf"))
        if not out:
            return
        margins = {
            "left": self._left.value(),
            "right": self._right.value(),
            "top": self._top.value(),
            "bottom": self._bottom.value(),
        }
        raw = self._pages_input.text().strip()
        indices = []
        if raw:
            try:
                indices = [int(p.strip()) - 1 for p in raw.split(",") if p.strip()]
            except ValueError:
                return self._show_error("Invalid page numbers.")
        self._run_worker(crop_pages, pdf, out, indices, margins, start_msg="Cropping…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Repair PDF page
# ---------------------------------------------------------------------------

class RepairPdfPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Repair PDF", "Attempt to repair corrupted or malformed PDF files", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        btn = QPushButton("Repair PDF")
        btn.clicked.connect(self._repair)
        self._add_to_content(btn)

        self._result_label = QLabel("")
        self._result_label.setWordWrap(True)
        self._add_to_content(self._result_label)

    def _repair(self):
        from src.core.repair import repair_pdf
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        out = self._save_dialog(self, "Save Repaired PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_repaired.pdf"))
        if not out:
            return
        self._run_worker(repair_pdf, pdf, out, start_msg="Repairing PDF…")

    def _on_worker_finished(self, result):
        if result["success"]:
            self._result_label.setText(f"✅ {result['message']}")
            self._progress.finish("Done!")
            QMessageBox.information(self, "Repaired", result["message"] + f"\n\nSaved to:\n{result['output_path']}")
        else:
            self._result_label.setText(f"❌ {result['message']}")
            self._show_error(result["message"])


# ---------------------------------------------------------------------------
# Organize Pages page
# ---------------------------------------------------------------------------

class OrganizePagesPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Organize Pages", "Reorder or delete pages from a PDF", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._file_drop.files_dropped.connect(self._load_pages)
        self._add_to_content(self._file_drop)

        list_grp = QGroupBox("Page Order (drag to reorder, select + delete key to remove)")
        list_layout = QVBoxLayout(list_grp)
        self._page_list = QListWidget()
        self._page_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._page_list.setMinimumHeight(150)
        self._page_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        list_layout.addWidget(self._page_list)

        del_btn = QPushButton("Delete Selected Pages")
        del_btn.setObjectName("secondaryBtn")
        del_btn.clicked.connect(self._delete_selected)
        list_layout.addWidget(del_btn)
        self._add_to_content(list_grp)

        btn = QPushButton("Apply & Save")
        btn.clicked.connect(self._save)
        self._add_to_content(btn)

        self._total_pages = 0

    def _load_pages(self, files: list) -> None:
        self._page_list.clear()
        if not files:
            return
        try:
            import fitz
            doc = fitz.open(files[0])
            self._total_pages = doc.page_count
            doc.close()
            for i in range(self._total_pages):
                self._page_list.addItem(QListWidgetItem(f"Page {i + 1}"))
        except Exception as exc:
            self._show_error(str(exc))

    def _delete_selected(self) -> None:
        for item in self._page_list.selectedItems():
            self._page_list.takeItem(self._page_list.row(item))

    def _save(self):
        from src.core.organizer import reorder_pages
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        if self._page_list.count() == 0:
            return self._show_error("No pages left to save.")
        out = self._save_dialog(self, "Save Organized PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_organized.pdf"))
        if not out:
            return
        new_order = []
        for i in range(self._page_list.count()):
            label = self._page_list.item(i).text()
            page_num = int(label.replace("Page ", "")) - 1
            new_order.append(page_num)
        self._run_worker(reorder_pages, pdf, out, new_order, start_msg="Organizing pages…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Watermark page
# ---------------------------------------------------------------------------

class WatermarkPage(BaseFeaturePage):
    def __init__(self, parent=None):
        super().__init__("Watermark", "Add or remove text/image watermarks from PDFs", parent)

        self._file_drop = FileDropWidget(accept_extensions=[".pdf"], multiple=False,
                                         label_text="Drop PDF here or click Browse")
        self._add_to_content(self._file_drop)

        # Add text watermark
        text_grp = QGroupBox("Add Text Watermark")
        text_form = QFormLayout(text_grp)
        self._wm_text = QLineEdit()
        self._wm_text.setPlaceholderText("Watermark text…")
        text_form.addRow("Text:", self._wm_text)
        self._wm_font_size = QDoubleSpinBox()
        self._wm_font_size.setRange(8, 200)
        self._wm_font_size.setValue(48)
        text_form.addRow("Font size:", self._wm_font_size)
        self._wm_angle = QDoubleSpinBox()
        self._wm_angle.setRange(-180, 180)
        self._wm_angle.setValue(45)
        text_form.addRow("Angle (°):", self._wm_angle)
        add_text_wm_btn = QPushButton("Add Text Watermark")
        add_text_wm_btn.clicked.connect(self._add_text_wm)
        text_form.addRow(add_text_wm_btn)
        self._add_to_content(text_grp)

        # Add image watermark
        img_grp = QGroupBox("Add Image Watermark")
        img_layout = QVBoxLayout(img_grp)
        self._wm_img_drop = FileDropWidget(
            accept_extensions=[".png", ".jpg", ".jpeg"],
            multiple=False,
            label_text="Drop watermark image here",
        )
        img_layout.addWidget(self._wm_img_drop)
        add_img_wm_btn = QPushButton("Add Image Watermark")
        add_img_wm_btn.clicked.connect(self._add_image_wm)
        img_layout.addWidget(add_img_wm_btn)
        self._add_to_content(img_grp)

        # Remove watermark
        rm_grp = QGroupBox("Remove Text Watermark")
        rm_form = QFormLayout(rm_grp)
        self._rm_wm_text = QLineEdit()
        self._rm_wm_text.setPlaceholderText("Text to remove…")
        rm_form.addRow("Watermark text:", self._rm_wm_text)
        rm_btn = QPushButton("Remove Watermark")
        rm_btn.clicked.connect(self._remove_wm)
        rm_form.addRow(rm_btn)
        self._add_to_content(rm_grp)

    def _add_text_wm(self):
        from src.core.watermark import add_text_watermark
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        text = self._wm_text.text().strip()
        if not text:
            return self._show_error("Please enter watermark text.")
        out = self._save_dialog(self, "Save Watermarked PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_watermarked.pdf"))
        if not out:
            return
        self._run_worker(
            add_text_watermark, pdf, out, text,
            font_size=self._wm_font_size.value(),
            angle=self._wm_angle.value(),
            start_msg="Adding text watermark…",
        )

    def _add_image_wm(self):
        from src.core.watermark import add_image_watermark
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        img = self._wm_img_drop.file
        if not img:
            return self._show_error("Please select a watermark image.")
        out = self._save_dialog(self, "Save Watermarked PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_watermarked.pdf"))
        if not out:
            return
        self._run_worker(add_image_watermark, pdf, out, img, start_msg="Adding image watermark…")

    def _remove_wm(self):
        from src.core.watermark import remove_watermark_text
        pdf = self._file_drop.file
        if not pdf:
            return self._show_error("Please select a PDF file.")
        text = self._rm_wm_text.text().strip()
        if not text:
            return self._show_error("Please enter the watermark text to remove.")
        out = self._save_dialog(self, "Save PDF", "PDF Files (*.pdf)",
                                pdf.replace(".pdf", "_no_watermark.pdf"))
        if not out:
            return
        self._run_worker(remove_watermark_text, pdf, out, text, start_msg="Removing watermark…")

    def _on_worker_finished(self, result):
        self._show_success(f"Saved to:\n{result}")


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------

PAGES = [
    ("home",         "🏠 Home",           None),
    # Convert
    ("pdf_to_excel",  "📊 PDF to Excel",   PdfToExcelPage),
    ("excel_to_pdf",  "📄 Excel to PDF",   ExcelToPdfPage),
    ("pdf_to_word",   "📝 PDF to Word",    PdfToWordPage),
    ("word_to_pdf",   "📝 Word to PDF",    WordToPdfPage),
    ("photos_to_pdf", "🖼️ Photos to PDF", PhotosToPdfPage),
    ("pdf_to_photos", "📸 PDF to Photos",  PdfToPhotosPage),
    # Edit
    ("compress",      "🗜️ Compress",       CompressPdfPage),
    ("editor",        "✏️ Editor",         PdfEditorPage),
    ("page_numbers",  "🔢 Page Numbers",   PageNumbersPage),
    # Security
    ("lock_unlock",   "🔐 Lock/Unlock",    LockUnlockPage),
    # Organize
    ("merge",         "🔗 Merge",          MergePdfsPage),
    ("split",         "✂️ Split",          SplitPdfPage),
    ("rotate",        "🔄 Rotate",         RotatePagesPage),
    ("crop",          "⬛ Crop",            CropPdfPage),
    ("repair",        "🔧 Repair",         RepairPdfPage),
    ("organize",      "📋 Organize",       OrganizePagesPage),
    # Watermark
    ("watermark",     "💧 Watermark",      WatermarkPage),
]

SECTIONS = [
    ("Convert",  ["pdf_to_excel", "excel_to_pdf", "pdf_to_word", "word_to_pdf", "photos_to_pdf", "pdf_to_photos"]),
    ("Edit",     ["compress", "editor", "page_numbers"]),
    ("Security", ["lock_unlock"]),
    ("Organize", ["merge", "split", "rotate", "crop", "repair", "organize"]),
    ("Watermark",["watermark"]),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Solutions")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────
        sidebar_scroll = QScrollArea()
        sidebar_scroll.setObjectName("sidebar")
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setFrameShape(QFrame.Shape.NoFrame)
        sidebar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sidebar_scroll.setFixedWidth(220)

        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebar")
        self._sidebar_layout = QVBoxLayout(sidebar_container)
        self._sidebar_layout.setContentsMargins(8, 8, 8, 8)
        self._sidebar_layout.setSpacing(2)

        # App title
        app_title = QLabel("📄 PDF Solutions")
        app_title.setStyleSheet("font-size: 15px; font-weight: bold; padding: 8px; color: #89B4FA;")
        self._sidebar_layout.addWidget(app_title)

        # Home button
        self._nav_buttons: dict = {}
        home_btn = QPushButton("🏠  Home")
        home_btn.setCheckable(True)
        home_btn.setChecked(True)
        home_btn.clicked.connect(lambda: self._navigate("home"))
        self._sidebar_layout.addWidget(home_btn)
        self._nav_buttons["home"] = home_btn

        # Section buttons
        page_map = {key: label for key, label, _ in PAGES}
        for section_name, page_keys in SECTIONS:
            section_label = QLabel(section_name)
            section_label.setStyleSheet(
                "font-size: 11px; font-weight: bold; color: #6C7086; "
                "padding: 8px 8px 2px 8px; letter-spacing: 1px;"
            )
            self._sidebar_layout.addWidget(section_label)

            for key in page_keys:
                label = page_map.get(key, key)
                btn = QPushButton(f"  {label}")
                btn.setCheckable(True)
                btn.clicked.connect(lambda checked, k=key: self._navigate(k))
                btn.setStyleSheet("text-align: left; padding-left: 20px;")
                self._sidebar_layout.addWidget(btn)
                self._nav_buttons[key] = btn

        self._sidebar_layout.addStretch()

        sidebar_scroll.setWidget(sidebar_container)
        main_layout.addWidget(sidebar_scroll)

        # ── Content area ─────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setObjectName("content")
        main_layout.addWidget(self._stack, stretch=1)

        # Build pages
        self._pages: dict = {}

        # Home
        home_page = HomePage()
        home_page.feature_selected.connect(self._navigate)
        self._stack.addWidget(home_page)
        self._pages["home"] = home_page

        # Feature pages
        for key, label, PageClass in PAGES:
            if PageClass is None:
                continue
            page = PageClass()
            self._stack.addWidget(page)
            self._pages[key] = page

        # Status bar
        self.statusBar().showMessage("Ready")

    def _navigate(self, page_key: str) -> None:
        if page_key not in self._pages:
            return

        # Uncheck all sidebar buttons
        for btn in self._nav_buttons.values():
            btn.setChecked(False)
        if page_key in self._nav_buttons:
            self._nav_buttons[page_key].setChecked(True)

        self._stack.setCurrentWidget(self._pages[page_key])
        self.statusBar().showMessage(f"Current: {page_key.replace('_', ' ').title()}")
