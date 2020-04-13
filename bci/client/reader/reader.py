import gzip
from .drivers import BinaryDriver, ProtobufDriver
from ...defaults import DEFAULT_FORMAT
from ...protocol.repr import user_repr, snapshot_repr

# TODO Replace it with generic driver
drivers = {
    'binary': BinaryDriver,
    'protobuf': ProtobufDriver,
}
"""dict: Dictionary of possible drivers."""


def find_driver(path, format):
    if format in drivers:
        return drivers[format](path)
    else:
        raise ValueError(f'unsupported sample format: {format}')


class Reader:
    """Encapsulates a sample's reader.

    Args:
        path (str): Path of the sample file.
        format (str): Format of the sample file.

    Attributes:
        path (str): Path of the sample file.
        format (str): Format of the sample file.

    Raises:
        ValueError: If `format` is not a supported sample format.

    """

    def __init__(self, path, format=None):
        self.path = path
        self.format = format or DEFAULT_FORMAT
        self._driver = find_driver(path, format)
        self._offset = 0
        self._open = gzip.open if path.endswith('.gz') else open
        self.user = self.driver.read_user()

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'path={self.path!r}, ' \
               f'format={self.format!r})'

    def __str__(self):
        return f'{self.user}'

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.driver.read_snapshot()
        except Exception as e:
            self.driver.close_file()
            raise StopIteration


def read(path, format):
    reader = Reader(path, format)
    print(user_repr(reader.user))
    for snapshot in reader:
        print(snapshot_repr(snapshot))
