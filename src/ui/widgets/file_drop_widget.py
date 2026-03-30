"""
Drag-and-drop file input widget.
"""

import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class FileDropWidget(QWidget):
    """
    A widget that accepts file drops or lets the user browse for files.

    Signals:
        files_dropped(list): emitted with a list of file paths.
    """

    files_dropped = Signal(list)

    def __init__(
        self,
        accept_extensions: list = None,
        multiple: bool = False,
        label_text: str = "Drop files here or click Browse",
        parent=None,
    ):
        super().__init__(parent)
        self._accept_extensions = [e.lower() for e in (accept_extensions or [])]
        self._multiple = multiple
        self._files: list = []

        self.setObjectName("fileDropWidget")
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        self._icon_label = QLabel("📂", self)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon_label.setStyleSheet("font-size: 32px; background: transparent;")
        layout.addWidget(self._icon_label)

        self._hint_label = QLabel(label_text, self)
        self._hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint_label.setStyleSheet("color: #A6ADC8; background: transparent;")
        layout.addWidget(self._hint_label)

        self._file_label = QLabel("", self)
        self._file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._file_label.setWordWrap(True)
        self._file_label.setStyleSheet("color: #89B4FA; background: transparent; font-size: 12px;")
        layout.addWidget(self._file_label)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._browse_btn = QPushButton("Browse…")
        self._browse_btn.setFixedWidth(120)
        self._browse_btn.clicked.connect(self._browse)
        btn_layout.addWidget(self._browse_btn)

        self._clear_btn = QPushButton("Clear")
        self._clear_btn.setObjectName("secondaryBtn")
        self._clear_btn.setFixedWidth(80)
        self._clear_btn.clicked.connect(self._clear)
        self._clear_btn.setVisible(False)
        btn_layout.addWidget(self._clear_btn)

        layout.addLayout(btn_layout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def files(self) -> list:
        """Return list of currently selected file paths."""
        return list(self._files)

    @property
    def file(self) -> str:
        """Return the first (or only) selected file path, or empty string."""
        return self._files[0] if self._files else ""

    def set_files(self, paths: list) -> None:
        """Programmatically set the selected files."""
        self._files = [p for p in paths if os.path.isfile(p)]
        self._update_labels()
        self.files_dropped.emit(self._files)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _browse(self) -> None:
        ext_filter = self._build_filter()
        if self._multiple:
            paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", ext_filter)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Select File", "", ext_filter)
            paths = [path] if path else []

        if paths:
            self._files = paths
            self._update_labels()
            self.files_dropped.emit(self._files)

    def _clear(self) -> None:
        self._files = []
        self._update_labels()
        self.files_dropped.emit([])

    def _build_filter(self) -> str:
        if not self._accept_extensions:
            return "All Files (*)"
        exts = " ".join(f"*{e}" for e in self._accept_extensions)
        return f"Supported Files ({exts});;All Files (*)"

    def _update_labels(self) -> None:
        if self._files:
            names = [os.path.basename(p) for p in self._files]
            self._file_label.setText("\n".join(names))
            self._clear_btn.setVisible(True)
        else:
            self._file_label.setText("")
            self._clear_btn.setVisible(False)

    # ------------------------------------------------------------------
    # Drag & Drop
    # ------------------------------------------------------------------

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        paths = []
        for url in urls:
            path = url.toLocalFile()
            if os.path.isfile(path):
                if self._accept_extensions:
                    _, ext = os.path.splitext(path)
                    if ext.lower() not in self._accept_extensions:
                        continue
                paths.append(path)
                if not self._multiple:
                    break

        if paths:
            self._files = paths
            self._update_labels()
            self.files_dropped.emit(self._files)
