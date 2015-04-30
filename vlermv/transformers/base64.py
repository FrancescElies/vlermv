from base64 import b64encode, b64decode

def to_path(path):
    return (b64encode(path.encode('utf-8')).decode('ascii'),)

def from_path(key):
    return b64decode(key[0]).decode('ascii')
