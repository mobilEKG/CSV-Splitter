import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QGroupBox, QCheckBox, QMessageBox, QProgressBar, QHBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from number_input import NumberLineEdit

class CSVSplitter(QWidget):
    DEFAULT_WINDOW_WIDTH = 500
    DEFAULT_WINDOW_HEIGHT = 360
    DEFAULT_SPACE = 20
    DEFAULT_LINES_PER_FILE = 200000

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Splitter")
        self.setFixedSize(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)

        self.layout = QVBoxLayout()

        # Section 1
        section1 = QGroupBox("Select CSV File")
        section1_layout = QVBoxLayout()
        section1_layout.setAlignment(Qt.AlignTop)
        section1_layout.setSpacing(self.DEFAULT_SPACE)
        section1_layout.setContentsMargins(self.DEFAULT_SPACE, self.DEFAULT_SPACE, self.DEFAULT_SPACE, self.DEFAULT_SPACE)
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
        section2_layout.setContentsMargins(self.DEFAULT_SPACE, self.DEFAULT_SPACE, self.DEFAULT_SPACE, self.DEFAULT_SPACE)        
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
        self.cancel_requested = False

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv);;Text Files (*.txt);;XML Files (*.xml);;All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.total_lines = self.get_total_lines(file_path)
            self.file_label.setText(f"Selected File: {os.path.basename(file_path)} ({self.total_lines:,} lines)")

    def get_total_lines(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)

    def cancel_split(self):
        self.cancel_requested = True

    def split_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return

        self.cancel_requested = False
        self.cancel_button.setEnabled(True)
        lines_per_file = self.line_input.value()
        include_header = self.include_header_checkbox.isChecked()

        base_name = os.path.basename(self.file_path)
        name, ext = os.path.splitext(base_name)
        output_dir = os.path.dirname(self.file_path)

        self.progress_bar.setMaximum(self.total_lines)
        self.progress_bar.setValue(0)
        # self.progress_bar.setVisible(True)

        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.readline() if include_header else ''
                self.progress_bar.setValue(1 if include_header else 0)
                lines = []
                file_index = 1
                written_files = 0

                for line_num, line in enumerate(f, start=1):
                    if self.cancel_requested:
                        QMessageBox.information(self, "Cancelled", "File splitting has been cancelled.")
                        # self.progress_bar.setVisible(False)
                        self.cancel_button.setEnabled(False)
                        return

                    lines.append(line)
                    self.progress_bar.setValue(self.progress_bar.value() + 1)
                    QApplication.processEvents()

                    if len(lines) >= lines_per_file:
                        written_files += 1
                        output_path = os.path.join(output_dir, f"{name}_{file_index}_of_XXX{ext}")
                        with open(output_path, 'w', encoding='utf-8') as out_file:
                            if include_header:
                                out_file.write(header)
                            out_file.writelines(lines)
                        lines = []
                        file_index += 1

                if lines and not self.cancel_requested:
                    written_files += 1
                    output_path = os.path.join(output_dir, f"{name}_{file_index}_of_XXX{ext}")
                    with open(output_path, 'w', encoding='utf-8') as out_file:
                        if include_header:
                            out_file.write(header)
                        out_file.writelines(lines)

            if not self.cancel_requested:
                for i in range(1, written_files + 1):
                    old_name = os.path.join(output_dir, f"{name}_{i}_of_XXX{ext}")
                    new_name = os.path.join(output_dir, f"{name}_{i}_of_{written_files}{ext}")
                    os.rename(old_name, new_name)

                # When no header is included the final loop may leave the
                # progress bar one step shy of the maximum.  Explicitly set the
                # value to ensure it reaches 100%.
                if self.progress_bar.value() < self.progress_bar.maximum():
                    self.progress_bar.setValue(self.progress_bar.maximum())

                QMessageBox.information(self, "Success", f"File successfully split into {written_files} parts.")

        finally:
            # self.progress_bar.setVisible(False)
            self.cancel_button.setEnabled(False)

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
