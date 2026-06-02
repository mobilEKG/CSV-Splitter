import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QGroupBox,
    QCheckBox,
    QMessageBox,
    QProgressBar,
    QHBoxLayout,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Qt, QThread, Signal, Slot
from number_input import NumberLineEdit
from split_logic import SplitCancelled, count_lines, split_csv_file


class CountLinesWorker(QObject):
    finished = Signal(str, int)
    error = Signal(str, str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            self.finished.emit(self.file_path, count_lines(self.file_path))
        except Exception as exc:
            self.error.emit(self.file_path, str(exc))


class SplitFileWorker(QObject):
    progress = Signal(int)
    finished = Signal(list)
    cancelled = Signal()
    error = Signal(str)

    def __init__(self, file_path, lines_per_file, include_header):
        super().__init__()
        self.file_path = file_path
        self.lines_per_file = lines_per_file
        self.include_header = include_header
        self.cancel_requested = False

    def request_cancel(self):
        self.cancel_requested = True

    @Slot()
    def run(self):
        try:
            output_files = split_csv_file(
                self.file_path,
                self.lines_per_file,
                self.include_header,
                progress_callback=self.progress.emit,
                should_cancel=lambda: self.cancel_requested,
            )
            self.finished.emit(output_files)
        except SplitCancelled:
            self.cancelled.emit()
        except Exception as exc:
            self.error.emit(str(exc))


class CSVSplitter(QWidget):
    DEFAULT_WINDOW_WIDTH = 500
    DEFAULT_WINDOW_HEIGHT = 360
    DEFAULT_SPACE = 20
    DEFAULT_LINES_PER_FILE = 200000

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Splitter")
        self.setFixedSize(
            self.DEFAULT_WINDOW_WIDTH,
            self.DEFAULT_WINDOW_HEIGHT,
        )

        self.layout = QVBoxLayout()

        # Section 1
        section1 = QGroupBox("Select CSV File")
        section1_layout = QVBoxLayout()
        section1_layout.setAlignment(Qt.AlignTop)
        section1_layout.setSpacing(self.DEFAULT_SPACE)
        section1_layout.setContentsMargins(
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
        )
        section1.setLayout(section1_layout)
        self.layout.addWidget(section1)

        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        section1_layout.addWidget(self.file_label)

        self.select_button = QPushButton("Select CSV File")
        self.select_button.clicked.connect(self.select_file)
        section1_layout.addWidget(self.select_button)

        # Section 2
        section2 = QGroupBox("Options")
        section2_layout = QVBoxLayout()
        section2_layout.setAlignment(Qt.AlignTop)
        section2_layout.setSpacing(self.DEFAULT_SPACE)
        section2_layout.setContentsMargins(
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
            self.DEFAULT_SPACE,
        )
        section2.setLayout(section2_layout)
        self.layout.addWidget(section2)

        line_input_layout = QHBoxLayout()
        section2_layout.addLayout(line_input_layout)
        self.line_input = NumberLineEdit(self)
        self.line_input.setValue(self.DEFAULT_LINES_PER_FILE)
        line_input_layout.addWidget(QLabel("Lines per file:"))
        line_input_layout.addWidget(self.line_input)

        self.include_header_checkbox = QCheckBox("Include header in each part")
        self.include_header_checkbox.setChecked(True)
        section2_layout.addWidget(self.include_header_checkbox)

        # QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        # self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # QHBoxLayout
        self.button_layout = QHBoxLayout()
        self.split_button = QPushButton("Split File")
        self.split_button.clicked.connect(self.split_file)
        self.button_layout.addWidget(self.split_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_split)
        self.cancel_button.setEnabled(False)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.file_path = ""
        self.total_lines = 0
        self.count_thread = None
        self.count_worker = None
        self.split_thread = None
        self.split_worker = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;XML Files (*.xml);;"
            "All Files (*)",
        )
        if file_path:
            self.file_path = file_path
            self.total_lines = 0
            self.progress_bar.setValue(0)
            self.file_label.setText(
                f"Counting lines in {os.path.basename(file_path)}..."
            )
            self.select_button.setEnabled(False)
            self.split_button.setEnabled(False)
            self.start_count_lines(file_path)

    def start_count_lines(self, file_path):
        self.count_thread = QThread(self)
        self.count_worker = CountLinesWorker(file_path)
        self.count_worker.moveToThread(self.count_thread)
        self.count_thread.started.connect(self.count_worker.run)
        self.count_worker.finished.connect(self.handle_count_finished)
        self.count_worker.error.connect(self.handle_count_error)
        self.count_worker.finished.connect(self.count_thread.quit)
        self.count_worker.error.connect(self.count_thread.quit)
        self.count_worker.finished.connect(self.count_worker.deleteLater)
        self.count_worker.error.connect(self.count_worker.deleteLater)
        self.count_thread.finished.connect(self.count_thread.deleteLater)
        self.count_thread.finished.connect(self.clear_count_worker)
        self.count_thread.start()

    def clear_count_worker(self):
        self.count_thread = None
        self.count_worker = None
        self.select_button.setEnabled(True)

    def handle_count_finished(self, file_path, total_lines):
        if file_path != self.file_path:
            return

        self.total_lines = total_lines
        self.file_label.setText(
            f"Selected File: {os.path.basename(file_path)} "
            f"({self.total_lines:,} lines)"
        )
        self.split_button.setEnabled(True)

    def handle_count_error(self, file_path, message):
        if file_path != self.file_path:
            return

        self.file_path = ""
        self.total_lines = 0
        self.file_label.setText("No file selected")
        self.split_button.setEnabled(False)
        QMessageBox.critical(
            self,
            "Error",
            f"Could not read {os.path.basename(file_path)}:\n{message}",
        )

    def cancel_split(self):
        if self.split_worker:
            self.split_worker.request_cancel()

    def split_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return

        lines_per_file = self.line_input.value()
        if lines_per_file <= 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Lines per file must be a positive number.",
            )
            return

        include_header = self.include_header_checkbox.isChecked()

        self.progress_bar.setMaximum(self.total_lines)
        self.progress_bar.setValue(0)
        self.select_button.setEnabled(False)
        self.split_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        self.split_thread = QThread(self)
        self.split_worker = SplitFileWorker(
            self.file_path,
            lines_per_file,
            include_header,
        )
        self.split_worker.moveToThread(self.split_thread)
        self.split_thread.started.connect(self.split_worker.run)
        self.split_worker.progress.connect(self.handle_split_progress)
        self.split_worker.finished.connect(self.handle_split_finished)
        self.split_worker.cancelled.connect(self.handle_split_cancelled)
        self.split_worker.error.connect(self.handle_split_error)
        self.split_worker.finished.connect(self.split_thread.quit)
        self.split_worker.cancelled.connect(self.split_thread.quit)
        self.split_worker.error.connect(self.split_thread.quit)
        self.split_worker.finished.connect(self.split_worker.deleteLater)
        self.split_worker.cancelled.connect(self.split_worker.deleteLater)
        self.split_worker.error.connect(self.split_worker.deleteLater)
        self.split_thread.finished.connect(self.split_thread.deleteLater)
        self.split_thread.finished.connect(self.clear_split_worker)
        self.split_thread.start()

    def handle_split_progress(self, lines_processed):
        next_value = self.progress_bar.value() + lines_processed
        self.progress_bar.setValue(min(next_value, self.progress_bar.maximum()))

    def handle_split_finished(self, output_files):
        if self.progress_bar.value() < self.progress_bar.maximum():
            self.progress_bar.setValue(self.progress_bar.maximum())

        QMessageBox.information(
            self,
            "Success",
            f"File successfully split into {len(output_files)} parts.",
        )

    def handle_split_cancelled(self):
        QMessageBox.information(
            self,
            "Cancelled",
            "File splitting has been cancelled.",
        )

    def handle_split_error(self, message):
        QMessageBox.critical(self, "Error", f"Could not split file:\n{message}")

    def clear_split_worker(self):
        self.split_thread = None
        self.split_worker = None
        self.cancel_button.setEnabled(False)
        self.select_button.setEnabled(True)
        self.split_button.setEnabled(bool(self.file_path))


def get_platform_icon():
    if getattr(sys, 'frozen', False):  # we are running in a bundle
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)

    if sys.platform.startswith("win"):
        icon_path = os.path.join(basedir, 'app_icon.ico')
    else:
        icon_path = os.path.join(basedir, 'app_icon.icns')

    return QIcon(icon_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = get_platform_icon()
    app.setWindowIcon(icon)

    splitter = CSVSplitter()
    splitter.show()

    sys.exit(app.exec())
