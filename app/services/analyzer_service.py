from services.excel_service import ExcelService

from pathlib import Path


class AnalyzerService:

    def __init__(self, video_service):

        self.video_service = video_service
        self.excel_service = ExcelService()

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

            frame_callback=frame_callback,

            progress_callback=progress_callback,

        )

        self.excel_service.add_video(

            file_name=Path(file_path).name,

            width=info["width"],

            height=info["height"],

            fps=info["fps"],

            frame_count=info["frame_count"],

            duration=info["duration"],

            sitting_time=0,

            standing_time=0,

            away_time=0,

            processed_date=""

        )

        self.excel_service.save()

        if log_callback:

            log_callback(

                "Finished."

            )