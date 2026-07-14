from PySide6.QtCore import QObject, Signal, Slot


class AnalyzerWorker(QObject):

    progress = Signal(int)
    log = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, analyzer_service, parent=None):
        super().__init__(parent)
        self.analyzer_service = analyzer_service
        self.queue = []
        self._stop_requested = False

    def set_queue(self, queue):
        self.queue = list(queue)

    def stop(self):
        self._stop_requested = True
        self.analyzer_service.stop()

    @Slot()
    def run(self):
        try:
            if not self.queue:
                self.log.emit("Queue is empty.")
                self.finished.emit()
                return

            total = len(self.queue)

            for index, file_path in enumerate(self.queue, start=1):
                if self._stop_requested:
                    break

                self.log.emit(f"Analyzing ({index}/{total}): {file_path.name}")

                self.analyzer_service.analyze_video(
                    file_path=file_path,
                    progress_callback=self.progress.emit,
                    log_callback=self.log.emit,
                )

            self.finished.emit()

        except Exception as ex:
            self.error.emit(str(ex))
            self.finished.emit()
