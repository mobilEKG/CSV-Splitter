import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FakeSignal:
    def __init__(self, *args, **kwargs):
        self._slots = []

    def connect(self, slot):
        self._slots.append(slot)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)


class FakeWidget:
    def closeEvent(self, event):
        event.accept()


class FakeMessageBox:
    @staticmethod
    def information(*args, **kwargs):
        raise AssertionError("close shutdown must not show message boxes")

    critical = information
    warning = information


def fake_slot(*args, **kwargs):
    def decorate(func):
        return func

    return decorate


def install_fake_pyside(monkeypatch):
    qtcore = types.ModuleType("PySide6.QtCore")
    qtcore.QObject = object
    qtcore.Qt = types.SimpleNamespace(AlignTop=0)
    qtcore.QThread = object
    qtcore.Signal = FakeSignal
    qtcore.Slot = fake_slot

    qtgui = types.ModuleType("PySide6.QtGui")
    qtgui.QIcon = object

    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    for name in (
        "QApplication",
        "QVBoxLayout",
        "QPushButton",
        "QFileDialog",
        "QLabel",
        "QGroupBox",
        "QCheckBox",
        "QProgressBar",
        "QHBoxLayout",
    ):
        setattr(qtwidgets, name, object)
    qtwidgets.QWidget = FakeWidget
    qtwidgets.QMessageBox = FakeMessageBox

    number_input = types.ModuleType("number_input")
    number_input.NumberLineEdit = object

    pyside = types.ModuleType("PySide6")
    monkeypatch.setitem(sys.modules, "number_input", number_input)
    monkeypatch.setitem(sys.modules, "PySide6", pyside)
    monkeypatch.setitem(sys.modules, "PySide6.QtCore", qtcore)
    monkeypatch.setitem(sys.modules, "PySide6.QtGui", qtgui)
    monkeypatch.setitem(sys.modules, "PySide6.QtWidgets", qtwidgets)


def load_gui_module(monkeypatch):
    install_fake_pyside(monkeypatch)
    spec = importlib.util.spec_from_file_location(
        "csv_splitter_gui_for_shutdown_test",
        ROOT / "csv-splitter.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeEvent:
    def __init__(self):
        self.accepted = False

    def accept(self):
        self.accepted = True


class FakeSplitWorker:
    def __init__(self):
        self.cancel_requested = False

    def request_cancel(self):
        self.cancel_requested = True


class FakeCountWorker(FakeSplitWorker):
    pass


class FakeThread:
    def __init__(self, running=True):
        self.running = running
        self.quit_called = False
        self.wait_called = False

    def isRunning(self):
        return self.running

    def quit(self):
        self.quit_called = True

    def wait(self):
        self.wait_called = True
        self.running = False


def test_close_event_cancels_and_waits_for_running_split(monkeypatch):
    gui = load_gui_module(monkeypatch)
    splitter = gui.CSVSplitter.__new__(gui.CSVSplitter)
    splitter.is_closing = False
    splitter.split_worker = FakeSplitWorker()
    splitter.split_thread = FakeThread()
    splitter.count_worker = None
    splitter.count_thread = FakeThread(running=False)
    event = FakeEvent()

    splitter.closeEvent(event)

    assert splitter.is_closing
    assert splitter.split_worker.cancel_requested
    assert splitter.split_thread.quit_called
    assert splitter.split_thread.wait_called
    assert not splitter.split_thread.isRunning()
    assert event.accepted


def test_close_event_cancels_and_waits_for_running_count(monkeypatch):
    gui = load_gui_module(monkeypatch)
    splitter = gui.CSVSplitter.__new__(gui.CSVSplitter)
    splitter.is_closing = False
    splitter.count_worker = FakeCountWorker()
    splitter.count_thread = FakeThread()
    splitter.split_worker = None
    splitter.split_thread = None
    event = FakeEvent()

    splitter.closeEvent(event)

    assert splitter.is_closing
    assert splitter.count_worker.cancel_requested
    assert splitter.count_thread.quit_called
    assert splitter.count_thread.wait_called
    assert not splitter.count_thread.isRunning()
    assert event.accepted


def test_count_worker_emits_cancelled_when_count_lines_is_cancelled(monkeypatch):
    gui = load_gui_module(monkeypatch)

    def fake_count_lines(file_path, should_cancel=None):
        assert file_path == "sample.csv"
        assert should_cancel()
        raise gui.SplitCancelled("cancelled")

    monkeypatch.setattr(gui, "count_lines", fake_count_lines)
    worker = gui.CountLinesWorker("sample.csv")
    cancelled_files = []
    errors = []
    worker.cancelled.connect(cancelled_files.append)
    worker.error.connect(lambda *args: errors.append(args))

    worker.request_cancel()
    worker.run()

    assert cancelled_files == ["sample.csv"]
    assert errors == []


def test_split_terminal_handlers_suppress_messages_during_close(monkeypatch):
    gui = load_gui_module(monkeypatch)
    splitter = gui.CSVSplitter.__new__(gui.CSVSplitter)
    splitter.is_closing = True

    splitter.handle_split_cancelled()
    splitter.handle_split_error("boom")
