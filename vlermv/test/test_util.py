import tempfile, time

import pytest

from .._util import split, _get_fn, method_or_name, safe_path

def test_split_empty():
    '''
    An error should be raised when you try to split an empty path.
    '''
    with pytest.raises(ValueError):
        split('')

testcases_split = [
    ('/', ('/',)),
    ('/abc', ('/', 'abc',)),
    ('123/abc', ('123', 'abc',)),
]

@pytest.mark.parametrize('path,expected', testcases_split)
def test_split(path, expected):
    assert split(path) == expected

def test_get_fn_success():
    with tempfile.NamedTemporaryFile('w') as tmp:
        tmp.file.write('abc')
        tmp.file.close()
        assert 'abc' == _get_fn(tmp.name, 'r', lambda fp: fp.read())

def test_get_fn_fail():
    def f(fp):
        time.sleep(0.1) # so mtime changes
        with open(fp.name, 'w') as fp2:
            fp2.write('other-process')
        return fp.read()

    with tempfile.NamedTemporaryFile('w') as tmp:
        tmp.file.write('this-process')
        tmp.file.close()
        with pytest.raises(EnvironmentError):
            _get_fn(tmp.name, 'r', f)

def test_method_or_name_not_str():
    class namespace:
        attribute = 8
    assert method_or_name(namespace, [2,9]) == [2,9]

def test_method_or_name_valid_str():
    class namespace:
        attribute = 8
    assert method_or_name(namespace, 'attribute') == 8

def test_method_or_name_invalid_str():
    class namespace:
        attribute = 8
    with pytest.raises(AttributeError):
        method_or_name(namespace, 'not_attribute')

tuple_path_testcases = [
    ('/home', 'abc', '/home', ('abc',)),
    ('/home', 'abc/def', '/home', ('abc', 'def')),
]

@pytest.mark.parametrize('dirpath, filename, root, safe', tuple_path_testcases)
def test_tuple_path(dirpath, filename, root, result):
    assert tuple_path(dirpath, filename, root) == result


    #    with pytest.raises(ValueError):
     #       safe_path(dirpath, filename, root)
