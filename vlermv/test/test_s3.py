import json

import pytest

from .._s3 import S3Vlermv, split

class FakeBucket:
    def __init__(self, **db):
        self.db = db
    def new_key(self, key):
        return FakeKey(self.db, key)
    def get_key(self, key):
        if key in self.db:
            return FakeKey(self.db, key)

class FakeKey:
    def __init__(self, db, key):
        self.db = db
        self.key = key
    def get_contents_as_string(self):
        return self.db[self.key]
    def get_contents_to_filename(self, filename):
        with open(filename, 'wb') as fp:
            fp.write(self.db[self.key])
    def set_contents_from_string(self, payload, **kwargs):
        self.db[self.key] = payload
    def set_contents_from_filename(self, filename, **kwargs):
        with open(filename, 'rb') as fp:
            self.db[self.key] = fp.read()

CONTRACT = {
    'bids': [],
    'contract': 'http://search.worldbank.org/wcontractawards/procdetails/OP00032101',
    'method.selection': 'QCBS ? Quality andCost-Based Selection',
    'price': 'INR 1,96,53,750',
    'project': None
}
PAYLOAD = json.dumps(CONTRACT).encode('utf-8')

def test_read():
    d = S3Vlermv('contracts', serializer = json,
                 bucket = FakeBucket(OP00032101 = PAYLOAD))
    assert d['OP00032101'] == CONTRACT

def test_write():
    fakebucket = FakeBucket()
    d = S3Vlermv('contracts', bucket = fakebucket, serializer = json)
    assert fakebucket.db == {}
    d['OP00032101'] = CONTRACT
    assert fakebucket.db == {'OP00032101': PAYLOAD}

def test_split():
    assert split('a/bb/cc') == ('a', 'bb', 'cc')
    assert split('one') == ('one',)
