# Data handling

exitaudit writes reports to the selected local directory. It has no telemetry or model API integration. HTML reports contain no remote assets.

Files are read locally. No APIs, uploads or external link requests are used. Reports include relative filenames, counts and findings, but omit document text, CSV values and link URLs. Filenames may still be confidential.

Symlinks, Windows reparse points, UNC paths and URL inputs are refused. A per-file limit of 64 MiB applies. Unreadable files, invalid text, malformed CSV and case collisions become explicit unverified findings. Keep the source and target stable during a run; protection against concurrent filesystem replacement is outside scope.

Link checks cover common inline and reference Markdown destinations. Nested parentheses, HTML links, anchors, embedded application objects and formatting fidelity are outside the parser's scope. Remote destinations are not checked. This is a file-level migration audit, not proof that an entire Notion workspace was exported. Extract archives yourself before comparison. A changed file is always flagged for review even when some CSV differences are harmless.

GitHub Actions uses read-only repository permissions and publishes no artifacts. Dependency installation contacts package providers. Report security issues privately to the repository owner without live credentials.
