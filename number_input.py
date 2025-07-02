
# number_input.py

from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt
import locale

locale.setlocale(locale.LC_ALL, '')


class NumberLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.textEdited.connect(self.format_input)

    def format_input(self, text):
        digits = ''.join(filter(str.isdigit, text))

        if digits:
            try:
                number = int(digits)
                formatted = locale.format_string("%d", number, grouping=True)
                self.blockSignals(True)
                self.setText(formatted)
                self.blockSignals(False)
            except ValueError:
                pass
        else:
            self.blockSignals(True)
            self.clear()
            self.blockSignals(False)

    def setValue(self, number):
        try:
            number = int(number)
            formatted = locale.format_string("%d", number, grouping=True)
            self.blockSignals(True)
            self.setText(formatted)
            self.blockSignals(False)
        except ValueError:
            self.clear()

    def value(self):
        digits = ''.join(filter(str.isdigit, self.text()))
        return int(digits) if digits else 0
