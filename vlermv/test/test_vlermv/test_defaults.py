import pickle, tempfile, os

import pytest

from .base import Base
from ..._vlermv import Vlermv

class TestDefaults(Base):
    def setup_method(self, method):
        self.directory = tempfile.mkdtemp()
        self.w = Vlermv(self.directory)

    def test_default_serializer(self):
        assert 'pickle' in self.w.serializer.__name__

    def test_default_transformer(self):
        'The default transformer should be very simple.'
        assert self.w.transformer.to_path('abc') == ('abc',)
        assert self.w.transformer.from_path(('abc',)) == 'abc'

        with pytest.raises(ValueError):
            self.w.transformer.to_path('abc/def')
        assert self.w.transformer.from_path(('abc', 'def')) == os.path.join('abc', 'def')

    def test_default_mutable(self):
        assert self.w.mutable

    def test_default_tempdir(self):
        assert self.w.tempdir == os.path.join(self.directory, '.tmp')
