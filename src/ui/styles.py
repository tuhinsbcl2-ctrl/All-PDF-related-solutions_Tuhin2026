"""
QSS stylesheets for the PDF Solutions application.
Provides dark and light themes.
"""

DARK_THEME = """
QMainWindow, QDialog {
    background-color: #1E1E2E;
    color: #CDD6F4;
}

QWidget {
    background-color: #1E1E2E;
    color: #CDD6F4;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

/* Sidebar */
#sidebar {
    background-color: #181825;
    border-right: 1px solid #313244;
    min-width: 220px;
    max-width: 220px;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #CDD6F4;
    text-align: left;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    font-size: 13px;
}

#sidebar QPushButton:hover {
    background-color: #313244;
}

#sidebar QPushButton:checked, #sidebar QPushButton[active="true"] {
    background-color: #2196F3;
    color: #FFFFFF;
}

#sidebar QLabel {
    color: #6C7086;
    font-size: 11px;
    font-weight: bold;
    padding: 8px 16px 4px 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Content area */
#content {
    background-color: #1E1E2E;
}

/* Cards */
.card {
    background-color: #24273A;
    border-radius: 10px;
    border: 1px solid #313244;
    padding: 16px;
}

/* Buttons */
QPushButton {
    background-color: #2196F3;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #1E88E5;
}

QPushButton:pressed {
    background-color: #1565C0;
}

QPushButton:disabled {
    background-color: #45475A;
    color: #6C7086;
}

QPushButton#secondaryBtn {
    background-color: #313244;
    color: #CDD6F4;
}

QPushButton#secondaryBtn:hover {
    background-color: #45475A;
}

/* Input fields */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #313244;
    color: #CDD6F4;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #2196F3;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    color: #CDD6F4;
    selection-background-color: #2196F3;
    border: 1px solid #45475A;
}

/* Progress bar */
QProgressBar {
    background-color: #313244;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 4px;
}

/* Scroll bars */
QScrollBar:vertical {
    background-color: #181825;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #45475A;
    border-radius: 4px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6C7086;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #181825;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #45475A;
    border-radius: 4px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #6C7086;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* Labels */
QLabel {
    color: #CDD6F4;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #CDD6F4;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #A6ADC8;
}

/* Group box */
QGroupBox {
    border: 1px solid #313244;
    border-radius: 8px;
    margin-top: 16px;
    padding: 12px;
    color: #CDD6F4;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #A6ADC8;
}

/* Checkboxes and radio buttons */
QCheckBox, QRadioButton {
    color: #CDD6F4;
    spacing: 6px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #45475A;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #2196F3;
    border: 1px solid #2196F3;
}

QRadioButton::indicator {
    border-radius: 8px;
}

QRadioButton::indicator:checked {
    background-color: #2196F3;
    border: 1px solid #2196F3;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 6px;
    background-color: #1E1E2E;
}

QTabBar::tab {
    background-color: #313244;
    color: #A6ADC8;
    padding: 8px 16px;
    border-radius: 4px;
    margin: 2px;
}

QTabBar::tab:selected {
    background-color: #2196F3;
    color: #FFFFFF;
}

QTabBar::tab:hover {
    background-color: #45475A;
}

/* List widgets */
QListWidget {
    background-color: #24273A;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 4px;
}

QListWidget::item {
    padding: 6px;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #2196F3;
    color: #FFFFFF;
}

QListWidget::item:hover {
    background-color: #313244;
}

/* Splitter */
QSplitter::handle {
    background-color: #313244;
}

/* Message/status bar */
QStatusBar {
    background-color: #181825;
    color: #6C7086;
    font-size: 12px;
}

/* Tool tips */
QToolTip {
    background-color: #313244;
    color: #CDD6F4;
    border: 1px solid #45475A;
    border-radius: 4px;
    padding: 4px 8px;
}

/* File drop widget */
#fileDropWidget {
    background-color: #24273A;
    border: 2px dashed #45475A;
    border-radius: 10px;
}

#fileDropWidget:hover {
    border-color: #2196F3;
}
"""

LIGHT_THEME = """
QMainWindow, QDialog {
    background-color: #F5F5F5;
    color: #212121;
}

QWidget {
    background-color: #F5F5F5;
    color: #212121;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

#sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E0E0E0;
    min-width: 220px;
    max-width: 220px;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #424242;
    text-align: left;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    font-size: 13px;
}

#sidebar QPushButton:hover {
    background-color: #F0F0F0;
}

#sidebar QPushButton:checked, #sidebar QPushButton[active="true"] {
    background-color: #2196F3;
    color: #FFFFFF;
}

#sidebar QLabel {
    color: #9E9E9E;
    font-size: 11px;
    font-weight: bold;
    padding: 8px 16px 4px 16px;
}

QPushButton {
    background-color: #2196F3;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #1E88E5;
}

QPushButton:pressed {
    background-color: #1565C0;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QPushButton#secondaryBtn {
    background-color: #E0E0E0;
    color: #424242;
}

QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BDBDBD;
    border-radius: 6px;
    padding: 6px 10px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #2196F3;
}

QProgressBar {
    background-color: #E0E0E0;
    border: none;
    border-radius: 4px;
    height: 8px;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 4px;
}

#fileDropWidget {
    background-color: #FFFFFF;
    border: 2px dashed #BDBDBD;
    border-radius: 10px;
}

#fileDropWidget:hover {
    border-color: #2196F3;
}
"""


def get_theme(theme_name: str = "dark") -> str:
    """Return QSS stylesheet string for the given theme ('dark' or 'light')."""
    if theme_name.lower() == "light":
        return LIGHT_THEME
    return DARK_THEME
