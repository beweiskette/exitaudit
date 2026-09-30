# Version 0.1 design

Compare a Markdown/CSV export with its migrated folder and identify missing files, changed content, broken local links and lost table rows.

The design was reviewed once through a read-only Claude adapter before implementation. That consultation received feature proposals and synthetic examples, not repository contents or credentials. Implementation and local verification were performed separately; the consultation was a design review, not a code audit.

The selected scope favours explicit user contracts and local evidence. Automatic uploads, model-generated pass criteria, background monitoring and publishing are excluded. This version makes no claim that the idea is unique or that it will attract a particular number of GitHub stars.

## Acceptance evidence

Tests cover missing files, exact attachment renames, ambiguous matches, duplicate CSV rows, UTF-8 BOM, invalid text, escaping links and unsafe paths. No external runtime is required.

## Deliberate limits

Files are read locally. No APIs, uploads or external link requests are used. Reports include relative filenames, counts and findings, but omit document text, CSV values and link URLs. Filenames may still be confidential.

Symlinks, Windows reparse points, UNC paths and URL inputs are refused. A per-file limit of 64 MiB applies. Unreadable files, invalid text, malformed CSV and case collisions become explicit unverified findings. Keep the source and target stable during a run; protection against concurrent filesystem replacement is outside scope.

Link checks cover common inline and reference Markdown destinations. Nested parentheses, HTML links, anchors, embedded application objects and formatting fidelity are outside the parser's scope. Remote destinations are not checked. This is a file-level migration audit, not proof that an entire Notion workspace was exported. Extract archives yourself before comparison. A changed file is always flagged for review even when some CSV differences are harmless.
