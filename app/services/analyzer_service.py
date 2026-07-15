from pathlib import Path

from services.excel_service import ExcelService
from services.statistics_service import StatisticsService


class AnalyzerService:

    def __init__(

        self,

        video_service,

        yolo_service,

    ):

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

                log_callback(

                    f"Cannot open : {file_path}"

                )

            return

        self.statistics.reset()

        info = self.video_service.get_video_info(

            capture

        )

        if log_callback:

            log_callback("")

            log_callback(

                "================================"

            )

            log_callback(

                f"Video : {Path(file_path).name}"

            )

            log_callback(

                f"Resolution : "

                f"{info['width']} x {info['height']}"

            )

            log_callback(

                f"FPS : {info['fps']:.2f}"

            )

            log_callback(

                f"Frames : "

                f"{info['frame_count']}"

            )

            log_callback(

                f"Duration : "

                f"{info['duration']:.1f} sec"

            )

            log_callback(

                "Reading frames..."

            )

        self.video_service.read_all_frames(

            capture,

            frame_callback=self.process_frame,

            progress_callback=progress_callback,

        )

        self.excel_service.add_video(

            file_name=Path(file_path).name,

            width=info["width"],

            height=info["height"],

            fps=info["fps"],

            frame_count=info["frame_count"],

            duration=info["duration"],

            sitting_time=self.statistics.sitting_frames / info["fps"],

            standing_time=self.statistics.standing_frames / info["fps"],

            away_time=self.statistics.away_frames / info["fps"],

            chair_frames=self.statistics.chair_frames,

            person_frames=self.statistics.person_frames,

            empty_frames=self.statistics.empty_frames,

            confidence=self.statistics.average_confidence(),

            processed_date=""

        )

        self.excel_service.save()

        if log_callback:

            log_callback(

                "Finished."

            )

    def process_frame(self, frame):

        persons = self.yolo_service.detect_persons(frame)

        person_detected = len(persons) > 0

        confidence = 0.0

        if person_detected:

            confidence = max(

                person["confidence"]

                for person in persons

            )

        self.statistics.add_frame(

            person=person_detected,

            chair=False,

            sitting=person_detected,

            standing=False,

            confidence=confidence,

    )