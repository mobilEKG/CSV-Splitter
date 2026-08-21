from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_keeps_primary_positioning_and_download_cta():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.startswith("# CSV Splitter：Windows 开源大文件 CSV 拆分工具")
    assert "下载最新版本" in readme
    assert "1,048,576 行" in readme
    assert "大型 CSV 文件" in readme


def test_cnb_pipeline_covers_review_main_and_release_events():
    pipeline = (ROOT / ".cnb.yml").read_text(encoding="utf-8")

    assert "pull_request:" in pipeline
    assert "  push:" in pipeline
    assert "  tag_push:" in pipeline
    assert "cnbcool/attachments:latest" in pipeline


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
    assert "https://cnb.cool/CodeAnt-2026/CSV-Splitter/-/releases/latest" in html
    assert "https://cnb.cool/CodeAnt-2026/CSV-Splitter" in html
    assert "Split files before Excel's 1,048,576-row limit gets in the way" in html
