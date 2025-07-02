import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from split_logic import split_csv_file


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
