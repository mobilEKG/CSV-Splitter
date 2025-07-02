import os
from typing import List


def split_csv_file(file_path: str, lines_per_file: int, include_header: bool = True) -> List[str]:
    """Split a text-based file into multiple smaller files.

    Parameters
    ----------
    file_path: str
        Path to the input CSV (or text) file.
    lines_per_file: int
        Maximum number of lines (excluding header) in each split file.
    include_header: bool, default True
        Whether to include the first line of the source file at the top of each
        split file.

    Returns
    -------
    List[str]
        Paths to the generated files.
    """
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    output_dir = os.path.dirname(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        header = f.readline() if include_header else ""
        lines = []
        file_index = 1
        written_files = 0
        output_paths: List[str] = []

        for line in f:
            lines.append(line)
            if len(lines) >= lines_per_file:
                written_files += 1
                output_path = os.path.join(output_dir, f"{name}_{file_index}_of_XXX{ext}")
                with open(output_path, "w", encoding="utf-8") as out_file:
                    if include_header:
                        out_file.write(header)
                    out_file.writelines(lines)
                output_paths.append(output_path)
                lines = []
                file_index += 1

        if lines:
            written_files += 1
            output_path = os.path.join(output_dir, f"{name}_{file_index}_of_XXX{ext}")
            with open(output_path, "w", encoding="utf-8") as out_file:
                if include_header:
                    out_file.write(header)
                out_file.writelines(lines)
            output_paths.append(output_path)

    for i in range(1, written_files + 1):
        old_name = os.path.join(output_dir, f"{name}_{i}_of_XXX{ext}")
        new_name = os.path.join(output_dir, f"{name}_{i}_of_{written_files}{ext}")
        os.rename(old_name, new_name)
        output_paths[i - 1] = new_name

    return output_paths

