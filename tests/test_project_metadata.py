from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_keeps_primary_positioning_and_download_cta():
    # Keep the shared default README English for both the CNB primary and the GitHub backup.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.startswith("# CSV Splitter: Open Source Large CSV File Splitter for Windows")
    assert "Download the latest Windows executable from CNB" in readme
    assert "1,048,576 rows" in readme
    assert "large CSV file" in readme
    assert "https://github.com/mobilEKG/CSV-Splitter" in readme
    assert "README.zh-CN.md" in readme
    assert "CSV_Splitter_macos.zip" in readme
    assert "CSV Splitter.app" in readme


def test_chinese_readme_is_available_as_a_linked_translation():
    chinese_readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    assert chinese_readme.startswith("# CSV Splitter：Windows 开源大文件 CSV 拆分工具")
    assert "README.md" in chinese_readme
    assert "https://github.com/mobilEKG/CSV-Splitter" in chinese_readme


def test_cnb_pipeline_covers_review_main_and_release_events():
    pipeline = (ROOT / ".cnb.yml").read_text(encoding="utf-8")

    assert "pull_request:" in pipeline
    assert "  push:" in pipeline
    assert "  tag_push:" in pipeline
    assert "cnbcool/attachments:latest" in pipeline
    assert "scripts/package_macos.sh" in pipeline
    assert "CSV_Splitter_macos.zip" in pipeline
    assert "v0.2.4" in pipeline
    assert "--output dist_upload/CSV_Splitter_macos" not in pipeline


def test_macos_package_metadata_is_present():
    plist = (ROOT / "packaging" / "macos" / "Info.plist").read_text(encoding="utf-8")
    script = (ROOT / "scripts" / "package_macos.sh").read_text(encoding="utf-8")

    assert "CSV_Splitter" in plist
    assert "CFBundlePackageType" in plist
    assert "ditto -c -k" in script
    assert "chmod 755" in script


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
