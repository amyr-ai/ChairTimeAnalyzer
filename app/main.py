import sys

print("Program started")

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    print("Creating QApplication")

    app = QApplication(sys.argv)

    print("Creating window")

    window = MainWindow()

    print("Showing window")

    window.show()

    print("Entering event loop")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()