from .drivers.binary import BinaryDriver
from .drivers.protobuf import ProtobufDriver
from ..utils.sample.repr import user_repr, snapshot_repr


class Reader:
    def __init__(self, path, fmt):
        self.path = path
        self.driver = _find_driver(path, fmt)
        self.user = self.driver.read_user()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.driver.read_snapshot()
        except Exception as e:
            self.driver.close_file()
            raise StopIteration


def _find_driver(path, fmt):
    if fmt == 'binary':
        return BinaryDriver(path)
    elif fmt == 'protobuf':
        return ProtobufDriver(path)
    else:
        raise ValueError(f'invalid file format: {fmt}')


def read(path, fmt):
    reader = Reader(path, fmt)
    print(user_repr(reader.user))
    for snapshot in reader:
        print(snapshot_repr(snapshot))
