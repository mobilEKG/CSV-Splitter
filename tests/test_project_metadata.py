from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_keeps_primary_positioning_and_download_cta():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.startswith(
        "# CSV Splitter: Open Source Large CSV File Splitter for Windows"
    )
    assert "Download the latest Windows executable" in readme
    assert "Excel's 1,048,576-row worksheet limit" in readme
    assert "large csv file splitter" in readme.lower()


def test_landing_page_has_search_and_social_metadata():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert (
        "<title>CSV Splitter: Open Source Large CSV File Splitter for Windows</title>"
        in html
    )
    assert (
        'name="description" content="Free open source Windows app for splitting large CSV, TXT, XML, and log files into smaller Excel-friendly parts with optional repeated headers."'
        in html
    )
    assert (
        'property="og:title" content="CSV Splitter: Open Source Large CSV File Splitter for Windows"'
        in html
    )
    assert "https://github.com/mobilEKG/CSV-Splitter/releases/latest" in html
    assert "Split files before Excel's 1,048,576-row limit gets in the way" in html
