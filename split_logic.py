import os
import uuid
from typing import Callable, List, Optional


ProgressCallback = Callable[[int], None]
CancelCallback = Callable[[], bool]

# A queued Qt signal for every source line becomes expensive on large files.
# Batch progress notifications while still checking cancellation per line.
PROGRESS_BATCH_SIZE = 1000


class SplitCancelled(RuntimeError):
    """Raised when a split operation is cancelled before completion."""


def count_lines(
    file_path: str,
    encoding: str = "utf-8-sig",
    should_cancel: Optional[CancelCallback] = None,
) -> int:
    """Count lines in a text file using strict decoding.

    Parameters
    ----------
    file_path: str
        Path to the input file.
    encoding: str, default "utf-8-sig"
        Text encoding used to read the file. Decode errors are raised instead
        of silently dropping bytes.
    should_cancel: callable, optional
        Called before and during counting. When it returns True,
        SplitCancelled is raised.
    """

    def check_cancelled() -> None:
        if should_cancel and should_cancel():
            raise SplitCancelled("Line count cancelled")

    total_lines = 0
    check_cancelled()
    with open(file_path, "r", encoding=encoding) as f:
        for _line in f:
            check_cancelled()
            total_lines += 1
    check_cancelled()
    return total_lines


def split_csv_file(
    file_path: str,
    lines_per_file: int,
    include_header: bool = True,
    encoding: str = "utf-8-sig",
    progress_callback: Optional[ProgressCallback] = None,
    should_cancel: Optional[CancelCallback] = None,
) -> List[str]:
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
    encoding: str, default "utf-8-sig"
        Text encoding used to read and write files. Decode errors are raised
        instead of silently dropping bytes.
    progress_callback: callable, optional
        Called with the number of newly processed source lines.
    should_cancel: callable, optional
        Called during processing. When it returns True, temporary output files
        are removed and SplitCancelled is raised.

    Returns
    -------
    List[str]
        Paths to the generated files.
    """
    if lines_per_file <= 0:
        raise ValueError("lines_per_file must be a positive integer")

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    output_dir = os.path.dirname(file_path)
    run_id = uuid.uuid4().hex
    temporary_paths: List[str] = []
    output_encoding = (
        "utf-8"
        if encoding.lower().replace("_", "-") == "utf-8-sig"
        else encoding
    )
    finalized_paths: List[str] = []
    pending_progress = 0
    active_output_file = None

    def check_cancelled() -> None:
        if should_cancel and should_cancel():
            raise SplitCancelled("Split cancelled")

    def flush_progress() -> None:
        nonlocal pending_progress
        if progress_callback and pending_progress:
            progress_callback(pending_progress)
            pending_progress = 0

    def report_progress(lines_processed: int) -> None:
        nonlocal pending_progress
        if not progress_callback:
            return

        pending_progress += lines_processed
        if pending_progress >= PROGRESS_BATCH_SIZE:
            flush_progress()

    def open_part(file_index: int, header: str):
        temporary_path = os.path.join(
            output_dir,
            f".{name}_{file_index}_of_{run_id}.tmp{ext}",
        )
        out_file = open(temporary_path, "x", encoding=output_encoding)
        temporary_paths.append(temporary_path)
        try:
            if include_header:
                out_file.write(header)
        except Exception:
            out_file.close()
            raise
        return out_file

    try:
        with open(file_path, "r", encoding=encoding) as f:
            header = f.readline() if include_header else ""
            if include_header and header:
                report_progress(1)

            file_index = 1
            lines_in_part = 0

            for line in f:
                check_cancelled()
                if active_output_file is None:
                    active_output_file = open_part(file_index, header)
                    lines_in_part = 0

                active_output_file.write(line)
                lines_in_part += 1
                report_progress(1)

                if lines_in_part >= lines_per_file:
                    active_output_file.close()
                    active_output_file = None
                    lines_in_part = 0
                    file_index += 1
                    check_cancelled()

            if active_output_file is not None:
                active_output_file.close()
                active_output_file = None

            # Flush a final partial batch so the GUI reaches the exact total.
            flush_progress()

        written_files = len(temporary_paths)
        output_paths = [
            os.path.join(output_dir, f"{name}_{i}_of_{written_files}{ext}")
            for i in range(1, written_files + 1)
        ]
        existing_paths = [path for path in output_paths if os.path.exists(path)]
        if existing_paths:
            raise FileExistsError(
                "Output file already exists: " + ", ".join(existing_paths)
            )

        for temporary_path, output_path in zip(temporary_paths, output_paths):
            if os.path.exists(output_path):
                raise FileExistsError(f"Output file already exists: {output_path}")
            os.replace(temporary_path, output_path)
            finalized_paths.append(output_path)

        return output_paths
    except Exception:
        if active_output_file is not None:
            active_output_file.close()
        for temporary_path in temporary_paths:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
        for finalized_path in finalized_paths:
            if os.path.exists(finalized_path):
                os.remove(finalized_path)
        raise
