import gzip

from .drivers import find_driver
from ..defaults import DEFAULT_FORMAT
from ..protocol.utils.display import display_user, display_snapshot


class Reader:
    """Represents a sample's reader.

    Attributes:
        path (str): Path of the sample file.
        format (str): Format of the sample file.

    Args:
        path (str): Path of the sample file.
        format (:obj:`str`, optional): Format of the sample file.
            Default to `DEFAULT_FORMAT`

    Raises:
        ValueError: If `format` is not supported.
        OSError: If a failure occurs while reading the sample file.

    """

    def __init__(self, path, format=None):
        self.path = str(path)
        self.format = format or DEFAULT_FORMAT
        _open = gzip.open if self.path.endswith('.gz') else open
        self._fp = _open(self.path, 'rb')
        try:
            self._driver = find_driver(self.format, self._fp)
            self.user = self._driver.read_user()
        except Exception as error:
            self._fp.close()
            raise error

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
            return self._driver.read_snapshot()
        except Exception:
            self._fp.close()
            raise StopIteration  # If the last snapshot read failed, just terminate


def read(path, format=None):
    """Reads the sample file from `path` and prints its content in a
    human-readable form.

    Args:
        path (str): Path of the sample file.
        format (:obj:`str`, optional): Format of the sample file.
            Default to `DEFAULT_FORMAT`.

    Raises:
        ValueError: If `format` is not a supported sample format.
        OSError: If a failure occurs while reading the sample file.

    """
    reader = Reader(path, format)
    display_user(reader.user)
    for snapshot in reader:
        display_snapshot(snapshot)
