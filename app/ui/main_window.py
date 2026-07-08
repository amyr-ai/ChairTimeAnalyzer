from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem


class MainWindow:

    def __init__(self):

        ui_file = QFile("app/ui/main_window.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)

        ui_file.close()

        self.window.btnBrowseFolder.clicked.connect(self.browse_folder)

    def load_video_list(self, folder):

        self.window.treeVideos.clear()

        video_extensions = {
            ".mp4",
            ".avi",
            ".mov",
            ".mkv"
        }

        folder = Path(folder)

        files = sorted(folder.iterdir())

        for file in files:

            if not file.is_file():
                continue

            if file.suffix.lower() not in video_extensions:
                continue

            item = QTreeWidgetItem()

            item.setText(0, file.name)
            item.setText(1, "Waiting")
            item.setText(2, "-")

            self.window.treeVideos.addTopLevelItem(item)

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self.window,
            "Select Video Folder"
        )

        if folder:

            self.window.txtVideoFolder.setText(folder)

            self.load_video_list(folder)

    def show(self):
        self.window.show()