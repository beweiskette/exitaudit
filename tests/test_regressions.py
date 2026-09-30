import unicodedata
import pytest
from test_compare import write
from exitaudit.compare import compare, csv_rows
from exitaudit.cli import main

def test_encoded_hash_filename(tmp_path):
    for root in (tmp_path/'a', tmp_path/'b'):
        write(root,'page.md','[issue](Issue%20%231.md)')
        write(root,'Issue #1.md','issue')
    assert compare(tmp_path/'a',tmp_path/'b')['broken_links'] == []

@pytest.mark.parametrize('body', ['`[x](absent.md)`', '~~~md\n[x](absent.md)\n~~~', '    [x](absent.md)\n', '``inline `[x](absent.md)` ``'])
def test_code_links_ignored(tmp_path, body):
    for root in (tmp_path/'a',tmp_path/'b'): write(root,'page.md',body)
    assert compare(tmp_path/'a',tmp_path/'b')['broken_links'] == []

def test_unicode_filename_equivalence(tmp_path):
    write(tmp_path/'a','café.md','hello')
    write(tmp_path/'b',unicodedata.normalize('NFD','café.md'),'hello')
    write(tmp_path/'a','index.md','[x](café.md)')
    write(tmp_path/'b','index.md','[x](café.md)')
    result = compare(tmp_path/'a',tmp_path/'b')
    assert result['status'] == 'pass', result
    assert result['renamed'] == []

def test_markdown_crlf_equivalence_and_rename(tmp_path):
    write(tmp_path/'a','old.md','unused')
    (tmp_path/'a'/'old.md').write_bytes(b'# Hello\r\n')
    write(tmp_path/'b','new.md','# Hello\n')
    result = compare(tmp_path/'a',tmp_path/'b')
    assert result['status'] == 'pass', result
    assert result['renamed'] == [{'from':'old.md','to':'new.md'}]

def test_notion_suffix_mapping_retains_content_change(tmp_path):
    write(tmp_path/'a','Notes '+ 'a'*32 +'.md','old')
    write(tmp_path/'b','Notes.md','new')
    result = compare(tmp_path/'a',tmp_path/'b')
    assert result['missing'] == []
    assert result['changed'] == ['Notes.md']

@pytest.mark.parametrize('cell', ['normal', 'x'*150000], ids=['normal', 'large'])
def test_csv_large_cells_and_trailing_empty_line(tmp_path, cell):
    path = tmp_path/'table.csv'
    path.write_text('header\n'+cell+'\n\n')
    columns, rows = csv_rows(path)
    assert columns == {'header'} and sum(rows.values()) == 1

def test_cli_error_has_reason(tmp_path, capsys):
    f = tmp_path/'file'; f.write_text('x')
    with pytest.raises(SystemExit) as error: main(['compare',str(f),str(f),'--out',str(tmp_path/'out')])
    assert error.value.code == 2
    assert 'export directory' in capsys.readouterr().err
