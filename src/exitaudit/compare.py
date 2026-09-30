import csv
import hashlib
import json
import re
from collections import Counter
from .inventory import inventory, MAX_FILE
from .links import check_links
from .safeio import local_path

def csv_rows(path):
    csv.field_size_limit(MAX_FILE)
    with local_path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, [])
        if len(set(header)) != len(header):
            raise ValueError('Duplicate CSV columns')
        rows = Counter()
        for row in reader:
            if not row:
                continue
            if len(row) != len(header):
                raise ValueError('Malformed CSV row')
            # Normalise column order without retaining contents in the report.
            value = sorted(zip(header, row))
            rows[hashlib.sha256(json.dumps(value, ensure_ascii=False).encode()).hexdigest()] += 1
    return set(header), rows

def compare(source, target):
    a, old, ae = inventory(source)
    b, new, be = inventory(target)
    unverified = [dict(item, side=side) for side, items in [('source', ae), ('target', be)] for item in items]
    missing = set(old) - set(new)
    added = set(new) - set(old)
    renamed, ambiguous = [], []
    for name in sorted(missing):
        matches = [f for f in added if new[f] == old[name]]
        source_matches = [f for f in missing if old[f] == old[name]]
        if len(matches) == len(source_matches) == 1:
            renamed.append({'from': name, 'to': matches[0]})
        elif matches:
            ambiguous.append(name)
    # Notion export IDs are discarded only for an unambiguous filename pair.
    def title(name):
        return re.sub(r' [0-9a-fA-F]{32}(?=\.(?:md|markdown|csv)$)', '', name)
    remaining_old = missing - {r['from'] for r in renamed}
    remaining_new = added - {r['to'] for r in renamed}
    for name in sorted(remaining_old):
        matches = [f for f in remaining_new if title(f) == title(name)]
        sources = [f for f in remaining_old if title(f) == title(name)]
        if len(matches) == len(sources) == 1:
            renamed.append({'from': name, 'to': matches[0]})
        elif matches and name not in ambiguous:
            ambiguous.append(name)
    missing -= {r['from'] for r in renamed}
    added -= {r['to'] for r in renamed}
    changed = sorted(f for f in old.keys() & new.keys() if old[f] != new[f])
    changed += sorted(r['to'] for r in renamed if old[r['from']] != new[r['to']])
    tables = []
    pairs = [(name, name) for name in sorted(old.keys() & new.keys())]
    pairs += [(r['from'], r['to']) for r in renamed]
    for source_name, name in pairs:
        if not name.lower().endswith('.csv'):
            continue
        try:
            columns_a, rows_a = csv_rows(old.paths[source_name])
            columns_b, rows_b = csv_rows(new.paths[name])
            tables.append({'file': name, 'lost_columns': len(columns_a - columns_b),
                           'added_columns': len(columns_b - columns_a),
                           'lost_rows': sum((rows_a - rows_b).values()),
                           'added_rows': sum((rows_b - rows_a).values())})
        except (ValueError, UnicodeError, OSError, csv.Error):
            unverified.append({'file': name, 'reason': 'invalid-csv', 'side': 'comparison'})
    broken, markdown_errors = check_links(b, new)
    unverified.extend(markdown_errors)
    attention = bool(missing or changed or ambiguous or broken or unverified)
    return {'schema': 1, 'status': 'attention' if attention else 'pass',
            'source_count': len(old), 'target_count': len(new), 'missing': sorted(missing),
            'changed': changed, 'added': sorted(added), 'renamed': renamed, 'ambiguous': ambiguous,
            'csv': tables, 'broken_links': broken, 'unverified': unverified,
            'scope': 'Files, common Markdown links and CSV rows. Formatting, HTML links and remote destinations are not verified.'}
