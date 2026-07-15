from pathlib import Path

import cv2

from PySide6.QtCore import (
    QFile,
    Qt,
)

from PySide6.QtGui import (
    QImage,
    QPixmap,
)

from PySide6.QtUiTools import QUiLoader

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QTreeWidgetItem,
)

from services.video_service import VideoService
from services.analyzer_service import AnalyzerService
from services.yolo_service import YOLOService

class MainWindow:

    def __init__(self):

        ui_file = QFile("app/ui/main_window.ui")

        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)

        ui_file.close()

        self.video_service = VideoService()

        self.yolo_service = YOLOService()

        self.analyzer_service = AnalyzerService(

             self.video_service,

             self.yolo_service,

        )
        
        self.current_folder = None

        self.video_queue = []

        self.connect_signals()

    def connect_signals(self):

        self.window.btnBrowseFolder.clicked.connect(
            self.browse_folder
        )

        self.window.treeVideos.itemDoubleClicked.connect(
            self.open_selected_video
        )

        self.window.actionAnalyze.triggered.connect(
            self.analyze_queue
        )

    def show(self):

        self.window.show()

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self.window,
            "Select Video Folder"
        )

        if not folder:
            return

        self.current_folder = Path(folder)

        self.window.txtVideoFolder.setText(folder)

        self.window.treeVideos.clear()

        self.video_queue.clear()

        video_extensions = {
            ".mp4",
            ".avi",
            ".mov",
            ".mkv",
        }

        for file in sorted(self.current_folder.iterdir()):

            if not file.is_file():
                continue

            if file.suffix.lower() not in video_extensions:
                continue

            self.video_queue.append(file)

            item = QTreeWidgetItem()

            item.setText(0, file.name)
            item.setText(1, "Waiting")
            item.setText(2, "-")

            self.window.treeVideos.addTopLevelItem(item)

        self.window.progressAnalysis.setValue(0)

        self.window.txtLog.clear()

        self.add_log(
            f"{len(self.video_queue)} video(s) loaded."
        )


    def open_selected_video(
        self,
        item,
        column,
    ):

        file_path = self.current_folder / item.text(0)

        ok, frame = self.video_service.read_first_frame(
            file_path
        )

        if not ok:

            self.add_log(
                "Cannot open video."
            )

            return
        persons = self.yolo_service.detect_persons(frame)
        self.add_log(
            f"Persons detected : {len(persons)}"
        )
        frame = self.video_service.draw_person_boxes(

            frame,

            persons

        )

        self.add_log(
            f"Persons detected : {len(persons)}"
        )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        height, width, channel = frame.shape

        image = QImage(
            frame.data,
            width,
            height,
            channel * width,
            QImage.Format.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(image)

        self.window.lblPreview.setPixmap(

            pixmap.scaled(

                self.window.lblPreview.size(),

                Qt.AspectRatioMode.KeepAspectRatio,

                Qt.TransformationMode.SmoothTransformation,

            )

        )

        self.add_log(
            f"Preview loaded : {file_path.name}"
        )

        
    def analyze_queue(self):

        if self.current_folder is None:

            self.add_log(
                "Please select a video folder."
            )

            return

        if len(self.video_queue) == 0:

            self.add_log(
                "Video queue is empty."
            )

            return

        self.window.progressAnalysis.setValue(0)

        total = self.window.treeVideos.topLevelItemCount()

        for row in range(total):

            item = self.window.treeVideos.topLevelItem(row)

            file_name = item.text(0)

            file_path = self.current_folder / file_name

            item.setText(1, "Processing")

            QApplication.processEvents()

            self.analyzer_service.analyze_video(

                file_path=file_path,

                progress_callback=self.update_progress,

                log_callback=self.add_log,

            )

            item.setText(1, "Done")

            QApplication.processEvents()

        self.window.progressAnalysis.setValue(100)

        self.add_log("")

        self.add_log(
            "All videos processed successfully."
        )



    def update_progress(self, value):

        self.window.progressAnalysis.setValue(value)

        QApplication.processEvents()


    def add_log(self, text):

        self.window.txtLog.appendPlainText(text)

        QApplication.processEvents()

    def clear_queue(self):

        self.video_queue.clear()

        self.window.treeVideos.clear()

        self.window.progressAnalysis.setValue(0)

        self.window.txtLog.clear()

        self.add_log("Queue cleared.")


    def refresh_queue(self):

        if self.current_folder is None:
            return

        self.browse_folder()


    def set_status(self, text):

        self.window.statusbar.showMessage(text)


    def reset_progress(self):

        self.window.progressAnalysis.setValue(0)


    def finish_progress(self):

        self.window.progressAnalysis.setValue(100)


    def closeEvent(self, event):

        self.add_log("Application closed.")

        event.accept()    