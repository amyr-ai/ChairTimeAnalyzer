from PySide6.QtWidgets import QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class MainWindow:

    def __init__(self):

        ui_file = QFile("app/ui/main_window.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)

        ui_file.close()

        self.window.btnBrowseFolder.clicked.connect(self.browse_folder)

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self.window,
            "Select Video Folder"
        )

        if folder:
            self.window.txtVideoFolder.setText(folder)

    def show(self):
        self.window.show()