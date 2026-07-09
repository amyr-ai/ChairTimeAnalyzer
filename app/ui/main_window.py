from pathlib import Path
import cv2
from PySide6.QtCore import QFile,Qt
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog,QTreeWidgetItem
from services.video_service import VideoService

class MainWindow:
    def __init__(self):
        ui_file=QFile('app/ui/main_window.ui')
        ui_file.open(QFile.ReadOnly)
        self.window=QUiLoader().load(ui_file)
        ui_file.close()
        self.video_service=VideoService()
        self.current_folder=None
        self.window.btnBrowseFolder.clicked.connect(self.browse_folder)
        self.window.treeVideos.itemDoubleClicked.connect(self.open_selected_video)

    def show(self):
        self.window.show()

    def browse_folder(self):
        folder=QFileDialog.getExistingDirectory(self.window,'Select Video Folder')
        if not folder:
            return
        self.current_folder=Path(folder)
        self.window.txtVideoFolder.setText(folder)
        self.window.treeVideos.clear()
        exts={'.mp4','.avi','.mov','.mkv'}
        for f in sorted(self.current_folder.iterdir()):
            if f.is_file() and f.suffix.lower() in exts:
                item=QTreeWidgetItem()
                item.setText(0,f.name)
                item.setText(1,'Waiting')
                item.setText(2,'-')
                self.window.treeVideos.addTopLevelItem(item)

    def open_selected_video(self,item,column):
        ok,frame=self.video_service.read_first_frame(self.current_folder/item.text(0))
        if not ok:
            self.window.txtLog.appendPlainText('Cannot open video')
            return
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h,w,ch=frame.shape
        img=QImage(frame.data,w,h,ch*w,QImage.Format_RGB888)
        pix=QPixmap.fromImage(img)
        self.window.lblPreview.setPixmap(pix.scaled(self.window.lblPreview.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.window.txtLog.appendPlainText('Preview loaded')
