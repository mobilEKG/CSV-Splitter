import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import split_logic
from split_logic import SplitCancelled, count_lines, split_csv_file


def test_split_csv_file(tmp_path):
    # Create a temporary CSV file with a header and five lines
    input_file = tmp_path / "sample.csv"
    content = "header1,header2\n" + "\n".join(f"val{i},val{i}" for i in range(5)) + "\n"
    input_file.write_text(content)

    # Split into files with at most 2 lines per part (excluding header)
    output_files = split_csv_file(str(input_file), lines_per_file=2, include_header=True)

    assert len(output_files) == 3

    expected_names = [
        tmp_path / "sample_1_of_3.csv",
        tmp_path / "sample_2_of_3.csv",
        tmp_path / "sample_3_of_3.csv",
    ]
    assert [os.path.abspath(p) for p in output_files] == [str(p) for p in expected_names]

    # Verify contents of each part
    parts = [p.read_text().splitlines() for p in expected_names]

    assert parts[0] == ["header1,header2", "val0,val0", "val1,val1"]
    assert parts[1] == ["header1,header2", "val2,val2", "val3,val3"]
    assert parts[2] == ["header1,header2", "val4,val4"]


def test_split_csv_file_without_header(tmp_path):
    input_file = tmp_path / "sample.txt"
    input_file.write_text("line0\nline1\nline2\n")

    output_files = split_csv_file(str(input_file), lines_per_file=2, include_header=False)

    assert [os.path.basename(p) for p in output_files] == [
        "sample_1_of_2.txt",
        "sample_2_of_2.txt",
    ]
    assert (tmp_path / "sample_1_of_2.txt").read_text().splitlines() == ["line0", "line1"]
    assert (tmp_path / "sample_2_of_2.txt").read_text().splitlines() == ["line2"]


def test_split_csv_file_rejects_non_positive_line_count(tmp_path):
    input_file = tmp_path / "sample.csv"
    input_file.write_text("header\nrow\n")

    with pytest.raises(ValueError, match="positive"):
        split_csv_file(str(input_file), lines_per_file=0)

    assert sorted(p.name for p in tmp_path.iterdir()) == ["sample.csv"]


def test_split_csv_file_does_not_overwrite_existing_output(tmp_path):
    input_file = tmp_path / "sample.csv"
    input_file.write_text("header\nrow1\nrow2\n")
    existing_output = tmp_path / "sample_1_of_2.csv"
    existing_output.write_text("keep me\n")

    with pytest.raises(FileExistsError, match="sample_1_of_2.csv"):
        split_csv_file(str(input_file), lines_per_file=1)

    assert existing_output.read_text() == "keep me\n"
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "sample.csv",
        "sample_1_of_2.csv",
    ]


def test_split_csv_file_raises_on_invalid_utf8(tmp_path):
    input_file = tmp_path / "bad.csv"
    input_file.write_bytes(b"header\nvalid\n\xff\n")

    with pytest.raises(UnicodeDecodeError):
        split_csv_file(str(input_file), lines_per_file=1)

    assert sorted(p.name for p in tmp_path.iterdir()) == ["bad.csv"]


def test_split_csv_file_cleans_up_temporary_files_when_cancelled(tmp_path):
    input_file = tmp_path / "sample.csv"
    input_file.write_text("header\nrow1\nrow2\nrow3\n")
    progress_calls = 0

    def track_progress(_lines_processed):
        nonlocal progress_calls
        progress_calls += 1

    def cancel_after_first_part():
        return progress_calls >= 3

    with pytest.raises(RuntimeError, match="cancel"):
        split_csv_file(
            str(input_file),
            lines_per_file=1,
            progress_callback=track_progress,
            should_cancel=cancel_after_first_part,
        )

    assert sorted(p.name for p in tmp_path.iterdir()) == ["sample.csv"]


def test_split_csv_file_finalizes_without_hard_links(tmp_path, monkeypatch):
    input_file = tmp_path / "sample.csv"
    input_file.write_text("header\nrow1\nrow2\n")

    def fail_if_hard_linked(_source, _destination):
        raise OSError("hard links are not supported")

    monkeypatch.setattr(split_logic.os, "link", fail_if_hard_linked)

    output_files = split_csv_file(str(input_file), lines_per_file=1)

    assert [os.path.basename(p) for p in output_files] == [
        "sample_1_of_2.csv",
        "sample_2_of_2.csv",
    ]
    assert (tmp_path / "sample_1_of_2.csv").read_text().splitlines() == [
        "header",
        "row1",
    ]
    assert (tmp_path / "sample_2_of_2.csv").read_text().splitlines() == [
        "header",
        "row2",
    ]
    assert not any(p.name.startswith(".sample_") for p in tmp_path.iterdir())


def test_count_lines_can_be_cancelled(tmp_path):
    input_file = tmp_path / "sample.csv"
    input_file.write_text("header\nrow1\nrow2\n")
    cancel_checks = 0

    def cancel_after_first_iteration():
        nonlocal cancel_checks
        cancel_checks += 1
        return cancel_checks > 1

    with pytest.raises(SplitCancelled, match="cancelled"):
        count_lines(str(input_file), should_cancel=cancel_after_first_iteration)
