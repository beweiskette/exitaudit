import json
import pytest
from exitaudit.compare import compare

def write(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def test_losses_renames_links_and_csv(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    for root in (a, b):
        write(root, 'page.md', '[missing](absent.md)\n')
    write(a, 'private.md', 'PRIVATE_BODY_SENTINEL')
    write(a, 'photo.bin', 'SYNTHETIC_ATTACHMENT')
    write(b, 'renamed.bin', 'SYNTHETIC_ATTACHMENT')
    write(a, 'table.csv', '\ufeffName,Age\nAlice,8\nBob,9\nBob,9\n')
    write(b, 'table.csv', 'Name,Age\nAlice,8\nBob,9\n')
    result = compare(a, b)
    assert result['status'] == 'attention'
    assert result['missing'] == ['private.md']
    assert result['renamed'] == [{'from': 'photo.bin', 'to': 'renamed.bin'}]
    assert result['csv'][0]['lost_rows'] == 1
    assert result['broken_links'][0]['file'] == 'page.md'
    assert 'PRIVATE_BODY_SENTINEL' not in json.dumps(result)
    assert 'Alice' not in json.dumps(result)

def test_ambiguous_hashes_not_treated_as_success(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    write(a, 'x.bin', 'x')
    write(b, 'a.bin', 'x')
    write(b, 'b.bin', 'x')
    result = compare(a, b)
    assert result['missing'] == ['x.bin']
    assert result['renamed'] == []
    assert result['ambiguous'] == ['x.bin']

def test_links_cannot_escape_and_markdown_not_renamed_by_hash(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    write(a, 'page.md', '[x](../private.txt)\n')
    write(b, 'page2.md', '[x](../private.txt)\n')
    result = compare(a, b)
    assert result['missing'] == ['page.md']
    assert result['broken_links'][0]['reason'] == 'outside-export'

def test_clean_and_invalid_utf8(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    write(a, 'a.md', 'same')
    write(b, 'a.md', 'same')
    assert compare(a, b)['status'] == 'pass'
    (b / 'a.md').write_bytes(b'\xff')
    assert compare(a, b)['unverified']

def test_symlink_not_followed(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    a.mkdir(); b.mkdir()
    private = tmp_path / 'private'
    private.write_text('SECRET')
    try:
        (a / 'leak.md').symlink_to(private)
    except OSError:
        pytest.skip('symlinks unavailable')
    result = compare(a, b)
    assert result['unverified']
    assert 'SECRET' not in json.dumps(result)
