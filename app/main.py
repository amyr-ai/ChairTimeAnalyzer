import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from services.yolo_service import YOLOService


def main():

    app = QApplication(sys.argv)

    print("----------------------------------------")
    print("PTA Starting...")
    print("----------------------------------------")

    print("Loading YOLO model...")

    yolo = YOLOService()

    print("YOLO Loaded Successfully")

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()