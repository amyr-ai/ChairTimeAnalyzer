from pathlib import Path

from services.excel_service import ExcelService
from services.statistics_service import StatisticsService


class AnalyzerService:

    def __init__(self, video_service, yolo_service):

        self.video_service = video_service
        self.yolo_service = yolo_service
        self.excel_service = ExcelService()
        self.statistics = StatisticsService()

    def analyze_video(
        self,
        file_path,
        progress_callback=None,
        log_callback=None,
        frame_callback=None,
    ):

        capture = self.video_service.open_video(file_path)

        if capture is None:
            if log_callback:
                log_callback(f"Cannot open : {file_path}")
            return

        self.statistics.reset()

        info = self.video_service.get_video_info(capture)

        fps = info["fps"]
        frame_count = info["frame_count"]
        duration = info["duration"]

        current_frame = 0
        last_sitting = False
        chair_initialized = False

        while True:

            ok, frame = capture.read()

            if not ok:
                break

            if not chair_initialized:

                self.yolo_service.detect_green_chair_once(frame)
                chair_initialized = True

            if current_frame % self.yolo_service.SKIP_FRAMES == 0:

                persons = self.yolo_service.detect_persons(frame)

                last_sitting = self.yolo_service.is_sitting(
                    persons
                )

            self.statistics.update(
                frame_number=current_frame,
                sitting=last_sitting,
            )

            if frame_callback:
                frame_callback(frame)

            if progress_callback:
                percent = int(current_frame * 100 / frame_count)
                progress_callback(percent)

            current_frame += 1

        self.statistics.finish(current_frame - 1)

        self.excel_service.add_video(
            file_name=Path(file_path).name,
            duration=duration,
            fps=fps,
            frame_count=frame_count,
            sessions=self.statistics.get_sessions(),
        )

        self.excel_service.save()

        capture.release()

        if log_callback:
            log_callback("Finished.")
