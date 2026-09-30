# Data handling

ExitAudit has no telemetry, update checks, cloud account or model API integration. Reports are written only to the chosen local output directory. HTML uses no remote scripts, fonts or images.

Files are read locally. No APIs, uploads or external link requests are used. Reports include relative filenames, counts and findings, but omit document text, CSV values and link URLs. Filenames may still be confidential.

Symlinks, Windows reparse points, UNC paths and URL inputs are refused. A per-file limit of 64 MiB applies. Unreadable files, invalid text, malformed CSV and case collisions become explicit unverified findings. Keep the source and target stable during a run; protection against concurrent filesystem replacement is outside scope.

Link checks cover common inline and reference Markdown destinations. Nested parentheses, HTML links, anchors, embedded application objects and formatting fidelity are outside the parser's scope. Remote destinations are not checked. This is a file-level migration audit, not proof that an entire Notion workspace was exported. Extract archives yourself before comparison. A changed file is always flagged for review even when some CSV differences are harmless.

Dependencies are installed separately from package providers. GitHub Actions checks out the source and runs the test suite on GitHub-hosted runners. Workflows receive read-only repository permissions and publish no artifacts. Review inputs and reports before sharing them. Keep synthetic examples in this repository; do not commit real credentials, exports or receipts.

If you find a security issue, report it privately to the repository owner without including live credentials or personal data.
