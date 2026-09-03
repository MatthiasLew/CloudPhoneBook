"""Entry point for CloudPhoneBook Desktop application."""

import sys
from pathlib import Path

# Add src and shared directories to sys.path automatically
current_dir = Path(__file__).resolve().parent
shared_dir = current_dir.parent.parent.parent / "packages" / "shared"

if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

if shared_dir.exists() and str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

from PySide6.QtWidgets import QApplication
from app.bootstrap import AppBootstrap


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("CloudPhoneBook")
    app.setOrganizationName("MatthiasLew")

    bootstrap = AppBootstrap(app)
    bootstrap.run()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
