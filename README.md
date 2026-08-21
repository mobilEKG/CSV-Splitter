# CSV Splitter: Open Source Large CSV File Splitter for Windows

CSV Splitter is a free, open-source desktop app for splitting large CSV, TXT, XML, and log files into smaller parts that are easier to open in Excel and other tools.

[Download the latest Windows executable from CNB](https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest) or run from source with Python. CNB is the primary repository and GitHub is the backup mirror.

[CNB primary repository](https://cnb.cool/CodeAnt-2026/CSV-Splitter) | [GitHub backup](https://github.com/mobilEKG/CSV-Splitter) | [中文说明](README.zh-CN.md)

## Why Use CSV Splitter?

Microsoft Excel worksheets are limited to 1,048,576 rows. When a source file is larger than that, CSV Splitter lets you choose a practical row count and generate numbered output files that stay easier to open, inspect, and share.

Use it when you need to:

- Split a large CSV file before Excel's 1,048,576-row worksheet limit gets in the way.
- Break large text-based exports into smaller numbered files.
- Keep the original header row at the top of every generated part.
- Use a simple Windows desktop GUI instead of command-line scripts.

## Screenshot

![CSV Splitter main window showing file selection, line count options, header inclusion, and split controls](images/Screenshot.png)

## Features

- Split CSV, TXT, XML, log, and other text-based files into numbered parts.
- Choose how many data lines should go into each output file.
- Optionally copy the source header row into every generated part.
- Prevent accidental overwrites of existing output files.
- Cancel long-running line counts or split jobs.
- Build a standalone Windows executable with PyInstaller.

## Download For Windows

1. Open the [latest CNB release](https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest).
2. Download `CSV_Splitter_windows.exe`.
3. Run the executable and select the file you want to split.

## Download For macOS

The macOS package currently supports Apple Silicon Macs only.

1. Open the [latest CNB release](https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest).
2. Download `CSV_Splitter_macos.zip`.
3. Open the ZIP, then double-click `CSV Splitter.app`.
4. If macOS shows a security warning, Control-click the app, choose Open, and confirm.

The ZIP is required because a direct download of a bare executable can lose its macOS execute permission.

## Run From Source

Install the required Python dependencies with:

```bash
pip install -r requirements.txt
```

Launch the graphical interface with:

```bash
python csv-splitter.py
```

Set "Lines per file" below your target row limit. When "Include header in each part" is enabled, the header row is added to each output file in addition to the selected data-line count.

## Build A Windows Executable

```bash
pyinstaller csv-splitter.py --clean --noupx --noconsole --noconfirm --onefile --windowed --icon=app_icon.ico --add-data "app_icon.ico;."
```

## Build A macOS Package

Run this on an Apple Silicon Mac with Python and the dependencies installed:

```bash
sh scripts/package_macos.sh
```

The script creates `dist/CSV_Splitter_macos.zip`. CNB hosted Linux runners cannot cross-build this package.

## Testing

Install pytest, then run the test suite:

```bash
pip install pytest
pytest -q
```

## License

This project is released under the MIT License.
