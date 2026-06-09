# CSV Splitter SEO Positioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve CSV-Splitter discoverability and conversion by making the repo visibly target "open source large CSV file splitter for Windows" and by adding a simple product landing page.

**Architecture:** Keep application behavior unchanged. Update repository-facing content in `README.md`, add a static GitHub Pages landing page in `docs/index.html`, and add metadata regression tests so future README/site edits do not remove the core keywords or download path.

**Tech Stack:** Python 3, pytest, static HTML/CSS, GitHub repository metadata, GitHub Pages from the `docs/` folder.

---

## Source Recommendation Interpreted For This Repo

The external SEO review rated CSV-Splitter as having a strong product keyword and a useful Excel row-limit angle, but weaker GitHub metadata, no standalone landing page, and a first screen that does not push "Download for Windows" strongly enough. This plan intentionally excludes the other project mentioned in that review and focuses only on `mobilEKG/CSV-Splitter`.

## File Structure

- Modify: `README.md`
  - Responsibility: GitHub search/result positioning, first-screen download CTA, user-facing explanation, and contributor/build instructions.
- Create: `docs/index.html`
  - Responsibility: Static product landing page with `<title>`, meta description, Open Graph tags, screenshot, and primary download CTA.
- Create: `docs/github-metadata.md`
  - Responsibility: Exact manual GitHub repository settings to apply for topics, description, website URL, and social preview.
- Create: `tests/test_project_metadata.py`
  - Responsibility: Fast regression checks for README and landing-page SEO/conversion copy.

## Task 1: Add Metadata Regression Tests

**Files:**
- Create: `tests/test_project_metadata.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_project_metadata.py` with:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_keeps_primary_positioning_and_download_cta():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.startswith(
        "# CSV Splitter: Open Source Large CSV File Splitter for Windows"
    )
    assert "Download the latest Windows executable" in readme
    assert "Excel's 1,048,576-row worksheet limit" in readme
    assert "large CSV file splitter" in readme.lower()


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
```

- [ ] **Step 2: Run the new tests and verify they fail**

Run:

```bash
pytest tests/test_project_metadata.py -q
```

Expected: FAIL because `README.md` still starts with `# CSV-Splitter` and `docs/index.html` does not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/test_project_metadata.py
git commit -m "test: add repository metadata regression checks"
```

## Task 2: Rewrite README First Screen And Project Positioning

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace `README.md` with the stronger project copy**

Replace the complete file with:

```markdown
# CSV Splitter: Open Source Large CSV File Splitter for Windows

CSV Splitter is a free, open-source desktop app for splitting large CSV, TXT, XML, and log files into smaller parts that are easier to open in Excel and other tools.

[Download the latest Windows executable](https://github.com/mobilEKG/CSV-Splitter/releases/latest) or run from source with Python.

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

1. Open the [latest release](https://github.com/mobilEKG/CSV-Splitter/releases/latest).
2. Download `CSV_Splitter_windows.exe`.
3. Run the executable and select the file you want to split.

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

## Testing

Install pytest, then run the test suite:

```bash
pip install pytest
pytest -q
```

## License

This project is released under the MIT License.
```

- [ ] **Step 2: Run the README-focused test**

Run:

```bash
pytest tests/test_project_metadata.py::test_readme_keeps_primary_positioning_and_download_cta -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: strengthen CSV Splitter README positioning"
```

## Task 3: Add Static GitHub Pages Landing Page

**Files:**
- Create: `docs/index.html`

- [ ] **Step 1: Create `docs/index.html`**

Create `docs/index.html` with:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CSV Splitter: Open Source Large CSV File Splitter for Windows</title>
  <meta name="description" content="Free open source Windows app for splitting large CSV, TXT, XML, and log files into smaller Excel-friendly parts with optional repeated headers.">
  <link rel="canonical" href="https://mobilekg.github.io/CSV-Splitter/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="CSV Splitter: Open Source Large CSV File Splitter for Windows">
  <meta property="og:description" content="Split large CSV and text files into smaller Excel-friendly parts with a free open-source Windows desktop app.">
  <meta property="og:url" content="https://mobilekg.github.io/CSV-Splitter/">
  <meta property="og:image" content="https://mobilekg.github.io/CSV-Splitter/images/Screenshot.png">
  <style>
    :root {
      --ink: #172018;
      --muted: #56635a;
      --paper: #f7f2e8;
      --leaf: #226f54;
      --leaf-dark: #154d3a;
      --line: #d8cdb8;
      --panel: #fffaf0;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(34, 111, 84, 0.20), transparent 34rem),
        linear-gradient(135deg, #fffaf0 0%, var(--paper) 52%, #e9ddc6 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.6;
    }

    main {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 56px 0;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(320px, 520px);
      gap: 48px;
      align-items: center;
    }

    .eyebrow {
      color: var(--leaf-dark);
      font-family: "Trebuchet MS", sans-serif;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }

    h1 {
      margin: 12px 0 16px;
      font-size: clamp(2.4rem, 7vw, 5.8rem);
      line-height: 0.92;
      letter-spacing: -0.06em;
    }

    .lede {
      max-width: 42rem;
      color: var(--muted);
      font-size: 1.24rem;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin: 28px 0;
    }

    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 48px;
      padding: 0 20px;
      border: 2px solid var(--leaf-dark);
      border-radius: 999px;
      color: var(--leaf-dark);
      font-family: "Trebuchet MS", sans-serif;
      font-weight: 700;
      text-decoration: none;
    }

    .button.primary {
      background: var(--leaf);
      color: white;
      box-shadow: 0 14px 30px rgba(21, 77, 58, 0.22);
    }

    .screenshot {
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: rgba(255, 250, 240, 0.72);
      box-shadow: 0 24px 70px rgba(23, 32, 24, 0.14);
    }

    .screenshot img {
      display: block;
      width: 100%;
      border-radius: 14px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      margin-top: 56px;
    }

    .card {
      min-height: 190px;
      padding: 24px;
      border: 1px solid var(--line);
      border-radius: 22px;
      background: rgba(255, 250, 240, 0.76);
    }

    .card h2 {
      margin: 0 0 10px;
      font-size: 1.25rem;
    }

    .card p {
      margin: 0;
      color: var(--muted);
    }

    @media (max-width: 840px) {
      main {
        padding-top: 32px;
      }

      .hero,
      .grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main>
    <section class="hero" aria-labelledby="title">
      <div>
        <p class="eyebrow">Free open source Windows app</p>
        <h1 id="title">Split large CSV files before Excel does.</h1>
        <p class="lede">CSV Splitter breaks large CSV, TXT, XML, and log files into smaller numbered parts with optional repeated headers, using a simple desktop interface.</p>
        <div class="actions">
          <a class="button primary" href="https://github.com/mobilEKG/CSV-Splitter/releases/latest">Download for Windows</a>
          <a class="button" href="https://github.com/mobilEKG/CSV-Splitter">View source on GitHub</a>
        </div>
        <p>Split files before Excel's 1,048,576-row limit gets in the way.</p>
      </div>
      <figure class="screenshot">
        <img src="../images/Screenshot.png" alt="CSV Splitter main window showing file selection, line count options, header inclusion, and split controls">
      </figure>
    </section>

    <section class="grid" aria-label="CSV Splitter benefits">
      <article class="card">
        <h2>Excel-friendly output</h2>
        <p>Choose a row count per part and create smaller files that are easier to open, inspect, and share.</p>
      </article>
      <article class="card">
        <h2>Header repetition</h2>
        <p>Keep the source header row at the top of every generated file so each part remains understandable on its own.</p>
      </article>
      <article class="card">
        <h2>No command line required</h2>
        <p>Select a file, set a line count, and split from a PySide6 desktop GUI.</p>
      </article>
    </section>
  </main>
</body>
</html>
```

- [ ] **Step 2: Run the landing-page test**

Run:

```bash
pytest tests/test_project_metadata.py::test_landing_page_has_search_and_social_metadata -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add docs/index.html
git commit -m "docs: add CSV Splitter landing page"
```

## Task 4: Add Manual GitHub Metadata Checklist

**Files:**
- Create: `docs/github-metadata.md`

- [ ] **Step 1: Create the metadata checklist**

Create `docs/github-metadata.md` with:

```markdown
# GitHub Metadata Checklist

These settings are applied in GitHub repository settings or the repository About panel. They are documented here so the discoverability work stays reviewable with the repo.

## Repository About

Description:

```text
Open source Windows app for splitting large CSV, TXT, XML, and log files into smaller Excel-friendly parts.
```

Website:

```text
https://mobilekg.github.io/CSV-Splitter/
```

Topics:

```text
csv-splitter
large-csv
file-splitter
python
pyside6
pyinstaller
windows-app
desktop-app
excel
txt-splitter
log-splitter
open-source
```

## GitHub Pages

Use these settings:

```text
Source: Deploy from a branch
Branch: main
Folder: /docs
```

## Social Preview

Upload a PNG, JPG, or GIF under 1 MB in the repository settings. Use a 1280 by 640 pixel image for best display.

Suggested preview text:

```text
CSV Splitter
Open Source Large CSV File Splitter for Windows
Download for Windows
```
```

- [ ] **Step 2: Commit**

```bash
git add docs/github-metadata.md
git commit -m "docs: document GitHub repository metadata"
```

## Task 5: Run Full Verification

**Files:**
- Verify: `README.md`
- Verify: `docs/index.html`
- Verify: `docs/github-metadata.md`
- Verify: `tests/test_project_metadata.py`

- [ ] **Step 1: Run all tests**

Run:

```bash
pytest -q
```

Expected: all tests pass.

- [ ] **Step 2: Check for placeholder language in plan-created files**

Run:

```bash
python - <<'PY'
from pathlib import Path

tokens = ["TB" + "D", "TO" + "DO", "implement" + " later", "fill" + " in details"]
paths = [Path("README.md"), Path("docs"), Path("tests/test_project_metadata.py")]
matches = []
for path in paths:
    files = path.rglob("*") if path.is_dir() else [path]
    for file_path in files:
        if not file_path.is_file():
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(token in line for token in tokens):
                matches.append(f"{file_path}:{line_number}:{line}")
if matches:
    print("\n".join(matches))
    raise SystemExit(1)
PY
```

Expected: exit code 0 with no matches printed.

- [ ] **Step 3: Inspect the diff**

Run:

```bash
git diff -- README.md docs/index.html docs/github-metadata.md tests/test_project_metadata.py
```

Expected: diff shows only README positioning updates, the new landing page, the metadata checklist, and metadata tests.

- [ ] **Step 4: Final commit if Task 5 made cleanup edits**

If Task 5 required cleanup edits, run:

```bash
git add README.md docs/index.html docs/github-metadata.md tests/test_project_metadata.py
git commit -m "docs: finalize CSV Splitter discovery updates"
```

Expected: commit created only when cleanup edits exist.

## Self-Review

Spec coverage:

- Stronger visible positioning: covered by Task 2 README H1 and Task 3 landing page title/H1.
- Add or improve GitHub topics: covered by Task 4 checklist with exact topic values.
- Stronger meta title and description: covered by Task 3 `<title>`, meta description, and Open Graph tags.
- Push "Download for Windows" harder: covered by Task 2 first-screen CTA and Task 3 primary button.
- Keep scope to CSV-Splitter only: all files and metadata refer only to `mobilEKG/CSV-Splitter`.

Placeholder scan:

- No placeholder marker text remains in this plan.

Type and path consistency:

- Tests use `ROOT / "docs" / "index.html"`, matching Task 3.
- Tests use `README.md`, matching Task 2.
- Manual metadata lives in `docs/github-metadata.md`, matching Task 4.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-06-09-csv-splitter-seo-positioning.md`. Two execution options:

1. Subagent-Driven (recommended) - Dispatch a fresh subagent per task, review between tasks, fast iteration.
2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints.
