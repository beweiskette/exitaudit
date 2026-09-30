# Design

Audit Markdown and CSV migrations for missing content and broken local links.

Paths are matched using Unicode NFC, while file access retains the original spelling. NFC/NFD and case collisions are reported as unverified. Markdown hashes ignore CRLF versus LF. Unique identical-content pairs can identify renamed documents and attachments. A trailing 32-digit Notion export ID can also be removed for an unambiguous filename pair; changed content remains a finding. Ambiguous matches stay unresolved.

Link parsing splits URLs before decoding their paths, so `Issue%20%231.md` resolves to `Issue #1.md`. Inline code, backtick or tilde fences and indented code lines are excluded. The parser handles common export syntax; full CommonMark parsing, nested parentheses and anchors remain outside scope.

CSV readers accept trailing blank lines and cells up to the 64 MiB file budget. Duplicate rows still count separately. CSV file byte changes are flagged even when row comparison finds no loss.

## Scope

Files are read locally. No APIs, uploads or external link requests are used. Reports include relative filenames, counts and findings, but omit document text, CSV values and link URLs. Filenames may still be confidential.

Symlinks, Windows reparse points, UNC paths and URL inputs are refused. A per-file limit of 64 MiB applies. Unreadable files, invalid text, malformed CSV and case collisions become explicit unverified findings. Keep the source and target stable during a run; protection against concurrent filesystem replacement is outside scope.

Link checks cover common inline and reference Markdown destinations. Nested parentheses, HTML links, anchors, embedded application objects and formatting fidelity are outside the parser's scope. Remote destinations are not checked. This is a file-level migration audit, not proof that an entire Notion workspace was exported. Extract archives yourself before comparison. A changed file is always flagged for review even when some CSV differences are harmless.
