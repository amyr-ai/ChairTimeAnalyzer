class StatisticsService:

    def __init__(self):

        self.reset()

    def reset(self):

        self.total_frames = 0

        self.person_frames = 0

        self.chair_frames = 0

        self.empty_frames = 0

        self.sitting_frames = 0

        self.standing_frames = 0

        self.away_frames = 0

        self.total_confidence = 0

        self.confidence_count = 0

    def add_frame(

        self,

        person=False,

        chair=False,

        sitting=False,

        standing=False,

        confidence=0

    ):

        self.total_frames += 1

        if person:
            self.person_frames += 1

        if chair:
            self.chair_frames += 1

        if not person:
            self.empty_frames += 1

        if sitting:
            self.sitting_frames += 1

        if standing:
            self.standing_frames += 1

        if not sitting and not standing:
            self.away_frames += 1

        if confidence > 0:

            self.total_confidence += confidence

            self.confidence_count += 1

    def average_confidence(self):

        if self.confidence_count == 0:
            return 0

        return self.total_confidence / self.confidence_count