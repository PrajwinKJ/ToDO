from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap

# 1. Resolve directly from main.py's location (ignores working directory issues)
icon_path = Path(__file__).resolve().parent.parent / "markAsDone.svg"

# 2. Print diagnostic info to your terminal
print("Path exists:", icon_path.exists(), "| Path:", icon_path)
print("Pixmap is null:", QPixmap(str(icon_path)).isNull())

# 3. Apply the icon
