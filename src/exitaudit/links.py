import posixpath
import re
from urllib.parse import unquote, urlsplit
from .safeio import local_path

def check_links(root, files):
    broken, unverified = [], []
    for name in sorted(files):
        if not name.lower().endswith(('.md', '.markdown')):
            continue
        try:
            text = local_path(root / name).read_text(encoding='utf-8-sig')
        except (UnicodeError, OSError, ValueError):
            unverified.append({'file': name, 'reason': 'unreadable-markdown'})
            continue
        # Common Markdown export syntax. Complex nested destinations are not parsed.
        text = re.sub(r'(?ms)^```.*?^```[^\n]*', '', text)
        targets = re.findall(r'!?\[[^\]\n]*\]\(\s*(<[^>]*>|[^\s)]+)', text)
        targets += re.findall(r'(?m)^\s*\[[^\]]+\]:\s*(<[^>]*>|\S+)', text)
        for index, target in enumerate(targets, 1):
            target = unquote(target.strip('<>'))
            try:
                url = urlsplit(target)
            except ValueError:
                broken.append({'file': name, 'link': index, 'reason': 'invalid-link'})
                continue
            if url.scheme in ('http', 'https', 'mailto', 'tel'):
                continue
            if not target or target.startswith('#'):
                continue
            path = posixpath.normpath(posixpath.join(posixpath.dirname(name), url.path.replace('\\', '/')))
            if url.scheme or url.netloc or target.startswith(('/', '\\')) or path == '..' or path.startswith('../'):
                reason = 'outside-export'
            elif path not in files and not any(f.startswith(path.rstrip('/') + '/') for f in files):
                reason = 'missing-target'
            else:
                continue
            # Do not expose query strings, fragments or arbitrary link contents.
            broken.append({'file': name, 'link': index, 'reason': reason})
    return broken, unverified
