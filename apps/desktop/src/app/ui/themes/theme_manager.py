"""Theme manager handling application styling."""

from pathlib import Path
from PySide6.QtWidgets import QApplication

LIGHT_THEME_QSS = """
QMainWindow, QDialog, QWidget {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
}

QLineEdit {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 12px;
}
QLineEdit:focus {
    border: 1px solid #2563eb;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
QPushButton#secondaryButton {
    background-color: #e2e8f0;
    color: #334155;
}
QPushButton#secondaryButton:hover {
    background-color: #cbd5e1;
}
QPushButton#dangerButton {
    background-color: #ef4444;
    color: #ffffff;
}

QTableView {
    background-color: #ffffff;
    color: #0f172a;
    gridline-color: #e2e8f0;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    alternate-background-color: #f1f5f9;
}

QHeaderView::section {
    background-color: #f1f5f9;
    color: #475569;
    padding: 8px;
    font-weight: bold;
    border: none;
    border-bottom: 2px solid #cbd5e1;
}

QStatusBar {
    background-color: #f1f5f9;
    color: #64748b;
    font-size: 12px;
}
"""


class ThemeManager:
    def __init__(self) -> None:
        self.qss_dir = Path(__file__).parent
        self.dark_qss_file = self.qss_dir / "default.qss"

    def apply_theme(self, app: QApplication, theme_name: str = "dark") -> None:
        if theme_name.lower() == "light":
            app.setStyleSheet(LIGHT_THEME_QSS)
        else:
            if self.dark_qss_file.exists():
                with open(self.dark_qss_file, "r", encoding="utf-8") as f:
                    app.setStyleSheet(f.read())
            else:
                app.setStyleSheet("")
