"""
Progress bar widget with label.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class ProgressWidget(QWidget):
    """
    A simple widget that shows a labelled progress bar.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._status_label = QLabel("", self)
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status_label)

        self._progress_bar = QProgressBar(self)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        layout.addWidget(self._progress_bar)

        self.hide()

    def start(self, message: str = "Processing…") -> None:
        """Show the widget and set to indeterminate mode."""
        self._status_label.setText(message)
        self._progress_bar.setRange(0, 0)  # indeterminate
        self.show()

    def set_value(self, value: int, message: str = "") -> None:
        """Set a concrete percentage (0-100)."""
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(value)
        if message:
            self._status_label.setText(message)
        self.show()

    def finish(self, message: str = "Done!") -> None:
        """Mark as complete."""
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(100)
        self._status_label.setText(message)

    def reset(self) -> None:
        """Hide and reset."""
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._status_label.setText("")
        self.hide()
