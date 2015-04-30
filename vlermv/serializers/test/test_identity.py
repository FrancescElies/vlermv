from .base import Base
from .. import identity_str, identity_bytes

class TestIdentityStr(Base):
    serializer = identity_str
    obj = 'abc'
    dumped_obj = 'abc'

class TestIdentityBytes(Base):
    serializer = identity_bytes
    obj = 'abc'.encode('ascii')
    dumped_obj = 'abc'.encode('ascii')
