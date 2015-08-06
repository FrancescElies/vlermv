import tempfile

from ._abstract import AbstractVlermv
from ._safe_buckets import SafeBuckets

class S3Vlermv(AbstractVlermv):
    buckets = SafeBuckets()

    def __init__(self, bucketname, *path, bucket = None, **kwargs):
        super(S3Vlermv, self).__init__(**kwargs)
        if bucket:
            self.bucket = bucket
        else:
            self.bucket = self.buckets[bucketname]

        self.base_directory = '/'.join(path)
        if self.base_directory != '':
            self.base_directory += '/'

    def __repr__(self):
        return 'S3Vlermv(%s/%s)' % (self.bucket.name, self.base_directory)

    def filename(self, index):
        return self.base_directory + super(S3Vlermv, self).filename(index)

    def from_filename(self, filename):
        i = len(self.base_directory)
        if filename[:i] == self.base_directory:
            return super(S3Vlermv, self).from_filename(filename[i:])
        else:
            raise ValueError('Filename must start with "%s".' % self.base_directory)

    def __setitem__(self, index, obj):
        keyname = self.filename(index)
        key = self.bucket.new_key(keyname)
        with tempfile.NamedTemporaryFile('w+' + self._b()) as tmp:
            self.serializer.dump(obj, tmp.file)
            tmp.file.close()
            key.set_contents_from_filename(tmp.name, replace = True)

    def __contains__(self, index):
        keyname = self.filename(index)
        return self.bucket.get_key(keyname) != None

    def __getitem__(self, index):
        keyname = self.filename(index)
        key = self.bucket.get_key(keyname)
        if key:
            with tempfile.NamedTemporaryFile('w+' + self._b()) as tmp:
                key.get_contents_to_filename(tmp.name)
                tmp.file.seek(0)
                value = self.serializer.load(tmp.file)
            return value
        else:
            raise KeyError(keyname)

    def keys(self):
        for k in self.bucket.list(prefix = self.base_directory):
            index = self.from_filename(k.name)
            if index != None:
                yield index

    def __delitem__(self, index):
        super(S3Vlermv, self).__delitem__(index)
        keyname = self.filename(index)
        self.bucket.delete_key(keyname)

    def __len__(self):
        return sum(1 for _ in self.keys())
