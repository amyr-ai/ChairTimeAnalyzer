from pathlib import Path

from PySide6.QtWidgets import QApplication


class AnalyzerService:

    def __init__(self, video_service):
        self.video_service = video_service

    def analyze_video(
        self,
        file_path,
        progress_callback=None,
        log_callback=None,
    ):

        capture = self.video_service.open_video(file_path)

        if capture is None:
            if log_callback:
                log_callback(f"Cannot open: {file_path}")
            return

        frame_count = int(capture.get(7))  # cv2.CAP_PROP_FRAME_COUNT

        if frame_count <= 0:
            frame_count = 1

        current = 0

        while True:

            ok, frame = capture.read()

            if not ok:
                break

            current += 1

            if progress_callback:
                progress = int(current * 100 / frame_count)
                progress_callback(progress)
                QApplication.processEvents()

        capture.release()

        if progress_callback:
            progress_callback(100)

        if log_callback:
            log_callback(f"Finished : {Path(file_path).name}")
