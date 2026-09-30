# Validation

Checked on 2026-09-30 with Python 3.11 on Windows.

Before these repairs: 10 collected tests. After: 21 collected, 19 passed and 2 skipped. The skipped cases require Windows symlink creation privileges. Linux CI runs those cases. New bug regressions were run against the previous implementation and observed failing before their fixes; the XML test strengthens existing escaping coverage.

Tests use local Markdown/CSV fixtures and cover encoded filenames, code spans and fences, Unicode path equivalence, document renames, Notion ID suffixes, CSV blank lines and large cells. This package needs neither Docker nor a browser.

The current wheel builds with `python -m pip wheel --no-deps .` using pip's isolated build environment. CLI help succeeds. German README validation with schreibwaechter and locale de-CH reports 0 errors and 0 warnings. Only synthetic test inputs were used.

CI results are available at [GitHub Actions](https://github.com/beweiskette/exitaudit/actions). See SECURITY.md for report contents and runtime boundaries.
