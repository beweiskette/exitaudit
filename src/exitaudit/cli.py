import argparse
import json
from .compare import compare
from .safeio import report

def main(argv=None):
    parser = argparse.ArgumentParser(description='Compare local Markdown/CSV export folders')
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('compare')
    command.add_argument('source')
    command.add_argument('target')
    command.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        result = compare(args.source, args.target)
        report(result, args.out)
        print(json.dumps({'status': result['status'], 'missing': len(result['missing']), 'changed': len(result['changed'])}))
        return 0 if result['status'] == 'pass' else 1
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Cannot compare exports : {exc}. Check local paths and permissions.\n')
