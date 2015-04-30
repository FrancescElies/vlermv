import os
import pickle
import tempfile
from shutil import rmtree

from ..vlermv import Vlermv
from .. import exceptions

# References
# http://pytest.org/latest/xunit_setup.html

class TestImmutableVlermv:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.default = Vlermv(self.tmp)
        self.mutable = Vlermv(self.tmp, mutable = True)
        self.immutable = Vlermv(self.tmp, mutable = False)

    def teardown_method(self):
        rmtree(self.tmp)

    def test_setitem(self):
        self.mutable['a'] = 3
        self.default['a'] = 3
        with self.assertRaises(PermissionError):
            self.immutable['a'] = 3

    def test_delitem(self):
        self.mutable['a'] = 3
        del(self.default['a'])

        self.mutable['a'] = 3
        del(self.mutable['a'])

        self.mutable['a'] = 3
        with self.assertRaises(PermissionError):
            del(self.immutable['a'])

    def test_kwarg(self):
        assert (self.default.mutable)
        assert (self.mutable.mutable)
        assert not (self.immutable.mutable)

class TestVlermv:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Vlermv(self.tmp)

    def teardown_method(self):
        rmtree(self.tmp)

    def test_cachedir(self):
        cachedir = self.tmp + 'aaa'
        w = Vlermv(cachedir)
        assert w.cachedir == cachedir

    def test_default_dump(self):
        w = Vlermv(self.tmp)
        assert w.serializer.dump == pickle.dump

    def test_repr(self):
        self.assertEqual(repr(self.w), "Vlermv('%s')" % self.tmp)
        self.assertEqual(str(self.w), "Vlermv('%s')" % self.tmp)

        self.assertEqual(str(Vlermv('/tmp/a"b"c"')), '''Vlermv('/tmp/a"b"c"')''')

    def test_setitem(self):
        self.w[("Tom's", 'favorite color')] = 'pink'
        with open(os.path.join(self.tmp, "Tom's", 'favorite color'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, 'pink')

    def test_getitem(self):
        with open(os.path.join(self.tmp, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        self.assertEqual(self.w['profession'], 'dada artist')

        with self.assertRaises(KeyError):
            self.w['not a file']

    def test_get(self):
        with open(os.path.join(self.tmp, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        self.assertEqual(self.w['profession'], 'dada artist')
        self.assertEqual(self.w.get('hobby','business intelligence'), 'business intelligence')

    def test_delitem1(self):
        dirname = os.path.join(self.tmp, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        del(self.w[['foo','bar']])
        self.assertFalse(os.path.exists(filename))
        self.assertFalse(os.path.exists(dirname))

        with self.assertRaises(KeyError):
            del(self.w['not a file'])

    def test_delitem2(self):
        dirname = os.path.join(self.tmp, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        with open(filename+'2', 'wb') as fp:
            pass
        del(self.w[['foo','bar']])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(dirname))

        with self.assertRaises(KeyError):
            del(self.w['not a file'])

    def test_contains(self):
        self.assertFalse('needle' in self.w)
        with open(os.path.join(self.tmp, 'needle'), 'wb'):
            pass
        self.assertTrue('needle' in self.w)

    def test_len(self):
        for i in range(100):
            self.w[i] = i
        assert len(self.w) == 100

    def test_update(self):
        self.w.update({'dictionary': {'a':'z'}})
        with open(os.path.join(self.tmp, 'dictionary'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, {'a':'z'})

        self.w.update([('tuple', (2,4,8))])
        expected = {'tuple': (2,4,8),  'dictionary': {'a':'z'}}
        self.assertEqual(len(self.w), len(expected))
        for key in expected.keys():
            self.assertEqual(self.w[key], expected[key])

    def test_iter(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.tmp, 'z'), 'wb'):
            pass

        observed = set(x for x in self.w)
        expected = {'a/b/c/d', 'z'}

        assert observed == expected

    def test_keys(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.tmp, 'z'), 'wb'):
            pass
        with open(os.path.join(self.tmp, '.tmp', 'lalala'), 'wb'):
            pass

        observed = set(self.w.keys())
        expected = {'a/b/c/d', 'z'}

        assert observed == expected

    def test_values(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(123, fp)
        with open(os.path.join(self.tmp, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.values())
        expected = {123,str}

        assert observed == expected

    def test_items(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(9, fp)
        with open(os.path.join(self.tmp, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.items())
        expected = {('a/b/c/d',9), ('z',str)}

        assert observed == expected

def test_mkdir():
    d = '/tmp/not a directory'
    w = Vlermv(d)
    if os.path.exists(d):
        rmtree(d)
    w[('abc','def','ghi')] = 3
    with open(os.path.join('/tmp/not a directory/abc/def/ghi'), 'rb') as fp:
        observed = pickle.load(fp)
    assert observed == 3
