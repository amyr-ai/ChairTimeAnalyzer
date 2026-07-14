import cv2

class VideoService:
    def read_first_frame(self,file_path):
        cap=cv2.VideoCapture(str(file_path))
        ok,frame=cap.read()
        cap.release()
        return ok,frame

def open_video(self, file_path):

    capture = cv2.VideoCapture(str(file_path))

    if not capture.isOpened():
        return None

    return capture