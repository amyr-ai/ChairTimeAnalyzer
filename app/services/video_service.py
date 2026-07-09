import cv2

class VideoService:
    def read_first_frame(self,file_path):
        cap=cv2.VideoCapture(str(file_path))
        ok,frame=cap.read()
        cap.release()
        return ok,frame
