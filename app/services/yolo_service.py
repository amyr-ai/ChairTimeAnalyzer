from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO


class YOLOService:

    PERSON_CLASS = 0
    SKIP_FRAMES = 10

    def __init__(self):

        model_path = Path("app/models/yolo11n.pt")
        self.model = YOLO(model_path)

        self.lower_green = np.array([35, 40, 40], dtype=np.uint8)
        self.upper_green = np.array([95, 255, 255], dtype=np.uint8)

        self.chair_range = None

    def detect(self, frame):

        return self.model.predict(
            source=frame,
            conf=0.30,
            verbose=False,
        )

    def detect_persons(self, frame):

        results = self.detect(frame)

        persons = []

        for result in results:
            for box in result.boxes:

                if int(box.cls[0]) != self.PERSON_CLASS:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                persons.append(
                    {
                        "bbox": (x1, y1, x2, y2),
                        "confidence": float(box.conf[0]),
                    }
                )

        return persons

    def detect_green_chair_once(self, frame):

        if self.chair_range is not None:
            return self.chair_range

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(
            hsv,
            self.lower_green,
            self.upper_green,
        )

        kernel = np.ones((7, 7), np.uint8)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        if not contours:
            return None

        contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(contour) < 2500:
            return None

        x, y, w, h = cv2.boundingRect(contour)

        self.chair_range = (x, x + w)

        return self.chair_range

    def person_center_x(self, person):

        x1, _, x2, _ = person["bbox"]

        return int((x1 + x2) / 2)

    def is_sitting(self, persons):

        if self.chair_range is None:
            return False

        if not persons:
            return False

        x1, x2 = self.chair_range

        center_x = self.person_center_x(persons[0])

        return x1 <= center_x <= x2
