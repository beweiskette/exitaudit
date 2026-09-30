# ExitAudit

Compare a Markdown/CSV export with its migrated folder and identify missing files, changed content, broken local links and lost table rows.

Version 0.1.0. [Deutsch](README.de.md). Python 3.11 or newer. MIT licence.

## Install

From a clone of this repository:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## Run

```sh
exitaudit compare examples/source examples/target --out outputs/check
```

The synthetic example contains a renamed attachment, a missing page and a lost CSV row. The command intentionally exits with status 1 and writes the findings to `report.json` and `report.html`.

Markdown and CSV files are paired by exact relative path. Other files may be recognised as renamed only when their SHA-256 hash has exactly one matching missing source and one added destination. Ambiguous matches stay unresolved. CSV comparison accounts for duplicate rows and column order; UTF-8 with or without BOM is accepted.

Reports are local JSON and self-contained HTML. Exit status is 0 for a pass, 1 for findings, and 2 for an input or runtime setup error. Commands do not publish reports or contact a model API.

## Boundaries

Files are read locally. No APIs, uploads or external link requests are used. Reports include relative filenames, counts and findings, but omit document text, CSV values and link URLs. Filenames may still be confidential.

Symlinks, Windows reparse points, UNC paths and URL inputs are refused. A per-file limit of 64 MiB applies. Unreadable files, invalid text, malformed CSV and case collisions become explicit unverified findings. Keep the source and target stable during a run; protection against concurrent filesystem replacement is outside scope.

Link checks cover common inline and reference Markdown destinations. Nested parentheses, HTML links, anchors, embedded application objects and formatting fidelity are outside the parser's scope. Remote destinations are not checked. This is a file-level migration audit, not proof that an entire Notion workspace was exported. Extract archives yourself before comparison. A changed file is always flagged for review even when some CSV differences are harmless.

## Verify

```sh
python -m pytest -q
```

Tests cover missing files, exact attachment renames, ambiguous matches, duplicate CSV rows, UTF-8 BOM, invalid text, escaping links and unsafe paths. No external runtime is required.

GitHub Actions runs tests on Windows and Linux. Integration jobs use synthetic local fixtures. No deployment or package publication workflow is configured. Dependency installation and browser/image downloads are explicit setup steps that contact their respective package providers.

See [DESIGN.md](DESIGN.md) for the scope decisions and [SECURITY.md](SECURITY.md) for data handling.
