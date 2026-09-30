import hashlib
import os
import unicodedata
from .safeio import local_path

MAX_FILE = 64 * 1024 * 1024

class FileIndex(dict):
    def __init__(self):
        super().__init__()
        self.paths = {}

def inventory(directory):
    root = local_path(directory)
    if not root.is_dir():
        raise ValueError('An export directory is required')
    files, errors, folded = FileIndex(), [], {}
    def walk(folder):
        try:
            entries = sorted(os.scandir(folder), key=lambda e: e.name)
        except OSError:
            errors.append({'file': folder.relative_to(root).as_posix(), 'reason': 'unreadable-directory'})
            return
        for entry in entries:
            path = folder / entry.name
            relative = unicodedata.normalize('NFC', path.relative_to(root).as_posix())
            try:
                local_path(path)
                if path.is_dir():
                    walk(path)
                    continue
                if not path.is_file() or path.stat().st_size > MAX_FILE:
                    raise ValueError('unsupported-or-large-file')
                if relative.casefold() in folded:
                    errors.append({'file': relative, 'reason': 'case-collision'})
                    continue
                folded[relative.casefold()] = relative
                data = path.read_bytes()
                if relative.lower().endswith(('.md', '.markdown')):
                    data = data.replace(b'\r\n', b'\n')
                files[relative] = hashlib.sha256(data).hexdigest()
                files.paths[relative] = path
            except (ValueError, OSError):
                errors.append({'file': relative, 'reason': 'unsafe-or-unreadable-file'})
    walk(root)
    return root, files, errors
