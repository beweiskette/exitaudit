import hashlib
import os
from .safeio import local_path

MAX_FILE = 64 * 1024 * 1024

def inventory(directory):
    root = local_path(directory)
    if not root.is_dir():
        raise ValueError('An export directory is required')
    files, errors, folded = {}, [], {}
    def walk(folder):
        try:
            entries = sorted(os.scandir(folder), key=lambda e: e.name)
        except OSError:
            errors.append({'file': folder.relative_to(root).as_posix(), 'reason': 'unreadable-directory'})
            return
        for entry in entries:
            path = folder / entry.name
            relative = path.relative_to(root).as_posix()
            try:
                local_path(path)
                if path.is_dir():
                    walk(path)
                    continue
                if not path.is_file() or path.stat().st_size > MAX_FILE:
                    raise ValueError('unsupported-or-large-file')
                if relative.casefold() in folded:
                    errors.append({'file': relative, 'reason': 'case-collision'})
                folded[relative.casefold()] = relative
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(65536), b''):
                        digest.update(chunk)
                files[relative] = digest.hexdigest()
            except (ValueError, OSError):
                errors.append({'file': relative, 'reason': 'unsafe-or-unreadable-file'})
    walk(root)
    return root, files, errors
