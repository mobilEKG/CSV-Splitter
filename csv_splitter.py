import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QSpinBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt

class CSVSplitter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Splitter")
        self.resize(400, 200)

        self.layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        self.select_button = QPushButton("Select CSV File")
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        self.line_count_spin = QSpinBox()
        self.line_count_spin.setMaximum(10000000)
        self.line_count_spin.setValue(200000)
        self.layout.addWidget(QLabel("Lines per file:"))
        self.layout.addWidget(self.line_count_spin)

        self.include_header_checkbox = QCheckBox("Include header in each part")
        self.include_header_checkbox.setChecked(True)
        self.layout.addWidget(self.include_header_checkbox)

        self.split_button = QPushButton("Split File")
        self.split_button.clicked.connect(self.split_file)
        self.layout.addWidget(self.split_button)

        self.setLayout(self.layout)

        self.file_path = ""
        self.total_lines = 0

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv);;Text Files (*.txt);;XML Files (*.xml);;All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.total_lines = self.get_total_lines(file_path)
            self.file_label.setText(f"Selected File: {os.path.basename(file_path)} ({self.total_lines} lines)")

    def get_total_lines(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)

    def split_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return

        lines_per_file = self.line_count_spin.value()
        include_header = self.include_header_checkbox.isChecked()

        base_name = os.path.basename(self.file_path)
        name, ext = os.path.splitext(base_name)
        output_dir = os.path.dirname(self.file_path)

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            header = f.readline() if include_header else ''
            lines = []
            file_index = 1
            written_files = 0

            for line_num, line in enumerate(f, start=1):
                lines.append(line)
                if len(lines) >= lines_per_file:
                    written_files += 1
                    output_path = os.path.join(output_dir, f"{name}_part{file_index}_of_XXX{ext}")
                    with open(output_path, 'w', encoding='utf-8') as out_file:
                        if include_header:
                            out_file.write(header)
                        out_file.writelines(lines)
                    lines = []
                    file_index += 1

            if lines:
                written_files += 1
                output_path = os.path.join(output_dir, f"{name}_part{file_index}_of_XXX{ext}")
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    if include_header:
                        out_file.write(header)
                    out_file.writelines(lines)

        # Rename all part files with correct total count
        for i in range(1, written_files + 1):
            old_name = os.path.join(output_dir, f"{name}_part{i}_of_XXX{ext}")
            new_name = os.path.join(output_dir, f"{name}_part{i}_of_{written_files}{ext}")
            os.rename(old_name, new_name)

        QMessageBox.information(self, "Success", f"File successfully split into {written_files} parts.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splitter = CSVSplitter()
    splitter.show()
    sys.exit(app.exec())
