from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


class ExcelService:

    def __init__(self):

        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)

        self.file_path = self.output_folder / "PTA_Report.xlsx"

        self.workbook = Workbook()

        self.sheet = self.workbook.active
        self.sheet.title = "Video Analysis"

        self.create_header()

    def create_header(self):

        headers = [

            "File Name",
            "Processed Date",

            "Width",
            "Height",
            "Resolution",

            "FPS",
            "Frame Count",
            "Duration (sec)",

            "Sitting Time (sec)",
            "Standing Time (sec)",
            "Away Time (sec)",

            "Sitting (%)",
            "Standing (%)",
            "Away (%)",

            "Chair Frames",
            "Person Frames",
            "Empty Frames",

            "Confidence",

            "Version",

            "Remarks",

        ]

        fill = PatternFill(
            fill_type="solid",
            fgColor="4F81BD"
        )

        for column, header in enumerate(headers, start=1):

            cell = self.sheet.cell(
                row=1,
                column=column
            )

            cell.value = header

            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )

            cell.fill = fill

            cell.alignment = Alignment(
                horizontal="center"
            )

    def add_video(

        self,

        file_name,

        width,

        height,

        fps,

        frame_count,

        duration,

        sitting_time=0,

        standing_time=0,

        away_time=0,

        chair_frames=0,

        person_frames=0,

        empty_frames=0,

        confidence=0,

        processed_date="",

        version="v0.3.1",

        remarks=""

    ):

        row = self.sheet.max_row + 1

        resolution = f"{width} x {height}"

        if duration > 0:

            sitting_percent = sitting_time * 100 / duration

            standing_percent = standing_time * 100 / duration

            away_percent = away_time * 100 / duration

        else:

            sitting_percent = 0
            standing_percent = 0
            away_percent = 0

        values = [

            file_name,
            processed_date,

            width,
            height,
            resolution,

            round(fps, 2),
            frame_count,
            round(duration, 1),

            round(sitting_time, 1),
            round(standing_time, 1),
            round(away_time, 1),

            round(sitting_percent, 2),
            round(standing_percent, 2),
            round(away_percent, 2),

            chair_frames,
            person_frames,
            empty_frames,

            round(confidence, 2),

            version,

            remarks,

        ]

        for col, value in enumerate(values, start=1):

            self.sheet.cell(
                row=row,
                column=col
            ).value = value

    def save(self):

        self.sheet.freeze_panes = "A2"

        self.sheet.auto_filter.ref = self.sheet.dimensions

        for column in self.sheet.columns:

            length = 0

            letter = get_column_letter(
                column[0].column
            )

            for cell in column:

                if cell.value is None:
                    continue

                length = max(
                    length,
                    len(str(cell.value))
                )

            self.sheet.column_dimensions[
                letter
            ].width = length + 3

        self.workbook.save(
            self.file_path
        )

    def get_file_path(self):

        return self.file_path