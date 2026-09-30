import posixpath
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from .safeio import local_path

def prose(text):
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        if fence:
            if re.match(r'^ {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', line):
                fence = None
            continue
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if match:
            fence = match[1]
        elif not line.startswith(('    ', '\t')):
            lines.append(line)
    # Inline spans can contain shorter backtick runs and line breaks.
    return re.sub(r'(?<!`)(`+)(?!`)([\s\S]*?)(?<!`)\1(?!`)', '', ''.join(lines))

def check_links(root, files):
    broken, unverified = [], []
    for name in sorted(files):
        if not name.lower().endswith(('.md', '.markdown')):
            continue
        try:
            text = local_path(getattr(files, 'paths', {}).get(name, root / name)).read_text(encoding='utf-8-sig')
        except (UnicodeError, OSError, ValueError):
            unverified.append({'file': name, 'reason': 'unreadable-markdown'})
            continue
        # Common Markdown export syntax. Complex nested destinations are not parsed.
        text = prose(text)
        targets = re.findall(r'!?\[[^\]\n]*\]\(\s*(<[^>]*>|[^\s)]+)', text)
        targets += re.findall(r'(?m)^\s*\[[^\]]+\]:\s*(<[^>]*>|\S+)', text)
        for index, target in enumerate(targets, 1):
            target = target.strip('<>')
            try:
                url = urlsplit(target)
            except ValueError:
                broken.append({'file': name, 'link': index, 'reason': 'invalid-link'})
                continue
            if url.scheme in ('http', 'https', 'mailto', 'tel'):
                continue
            if not target or target.startswith('#'):
                continue
            decoded = unicodedata.normalize('NFC', unquote(url.path)).replace('\\', '/')
            path = posixpath.normpath(posixpath.join(posixpath.dirname(name), decoded))
            if url.scheme or url.netloc or decoded.startswith('/') or path == '..' or path.startswith('../'):
                reason = 'outside-export'
            elif path not in files and not any(f.startswith(path.rstrip('/') + '/') for f in files):
                reason = 'missing-target'
            else:
                continue
            # Do not expose query strings, fragments or arbitrary link contents.
            broken.append({'file': name, 'link': index, 'reason': reason})
    return broken, unverified
