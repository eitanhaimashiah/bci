import gzip
import pathlib
import importlib
import inspect
import sys

from ..defaults import DEFAULT_FORMAT
from ..protocol.utils import display_user, display_snapshot


class Reader:
    """Represents a sample's reader.

    Args:
        path (str): Path of the sample file.
        format (:obj:`str`, optional): Format of the sample file.
            Default to `DEFAULT_FORMAT`

    Attributes:
        path (str): Path of the sample file.
        format (str): Format of the sample file.

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
        except Exception as e:
            self._fp.close()
            raise e

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


def find_driver(format, stream):
    """Finds the appropriate driver according to `format`.

    Args:
        format (str): Format of the sample file.
        stream (IOBase): Stream representing the sample file.

    Returns:
        The appropriate driver according to `format`.

    Raises:
        ValueError: If `format` is not supported.

    """
    # Import all modules of the drivers
    modules = []
    drivers_dir = pathlib.Path(__file__).absolute().parent / 'drivers'
    sys.path.insert(0, str(drivers_dir.parent))
    for path in drivers_dir.iterdir():
        if path.suffix == '.py' and not path.name.startswith('_'):
            package = '.'.join([p.name for p in drivers_dir.parents][1::-1])
            modules.append(importlib.import_module(
                f'.{drivers_dir.name}.{path.stem}',
                package=package))

    # Find the appropriate driver class for `format`
    for module in modules:
        for key, value in module.__dict__.items():
            if key.endswith('Driver') and inspect.isclass(value)\
                    and value.format == format:
                return value(stream)

    raise ValueError(f'unknown format: {format}')


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
