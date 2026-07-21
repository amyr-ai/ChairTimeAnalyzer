class StatisticsService:

    def __init__(self):

        self.reset()

    def reset(self):

        self.sessions = []

        self.is_sitting = False

        self.start_frame = None

        self.end_frame = None

    def update(

        self,

        frame_number,

        sitting,

    ):

        # شروع یک Session

        if sitting and not self.is_sitting:

            self.is_sitting = True

            self.start_frame = frame_number

            return

        # پایان Session

        if (not sitting) and self.is_sitting:

            self.is_sitting = False

            self.end_frame = frame_number - 1

            self.sessions.append(

                {

                    "start_frame": self.start_frame,

                    "end_frame": self.end_frame,

                }

            )

            self.start_frame = None

            self.end_frame = None

    def finish(

        self,

        last_frame,

    ):

        if self.is_sitting:

            self.sessions.append(

                {

                    "start_frame": self.start_frame,

                    "end_frame": last_frame,

                }

            )

            self.is_sitting = False

    def get_sessions(

        self,

    ):

        return self.sessions