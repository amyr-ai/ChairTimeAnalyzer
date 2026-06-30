from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chair Time Analyzer")
        self.resize(1100, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title = QLabel("Chair Time Analyzer")
        layout.addWidget(title)

        central_widget.setLayout(layout)