from pathlib import Path

from ultralytics import YOLO


class YOLOService:

    def __init__(self):

        model_path = Path("app/models/yolo11n.pt")

        self.model = YOLO(model_path)

    def detect(self, frame):

        return self.model.predict(

            source=frame,

            conf=0.30,

            verbose=False

        )

    def detect_persons(self, frame):

        results = self.detect(frame)

        persons = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                if cls != 0:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                persons.append(

                    {

                        "bbox": (

                            int(x1),

                            int(y1),

                            int(x2),

                            int(y2),

                        ),

                        "confidence": float(box.conf[0]),

                    }

                )

        return persons