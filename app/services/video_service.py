import cv2


class VideoService:

    def open_video(self, file_path):

        capture = cv2.VideoCapture(str(file_path))

        if not capture.isOpened():
            return None

        return capture

    def read_first_frame(self, file_path):

        capture = self.open_video(file_path)

        if capture is None:
            return False, None

        ok, frame = capture.read()

        capture.release()

        return ok, frame

    def get_video_info(self, capture):

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = capture.get(cv2.CAP_PROP_FPS)

        frame_count = int(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if fps > 0:
            duration = frame_count / fps
        else:
            duration = 0

        return {

            "width": width,

            "height": height,

            "fps": fps,

            "frame_count": frame_count,

            "duration": duration,

        }

    def read_all_frames(

        self,

        capture,

        frame_callback=None,

        progress_callback=None,

    ):

        info = self.get_video_info(capture)

        total = max(info["frame_count"], 1)

        current = 0

        while True:

            ok, frame = capture.read()

            if not ok:
                break

            current += 1

            if frame_callback:

                frame_callback(frame)

            if progress_callback:

                progress = int(
                    current * 100 / total
                )

                progress_callback(progress)

        capture.release()

        return info