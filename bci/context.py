import pathlib
import datetime as dt

_ROOT = pathlib.Path(__file__).absolute().parent.parent
_DATA_DIR = _ROOT / 'data'


class Context:
    def __init__(self, data_dir=_DATA_DIR):
        self.data_dir = data_dir
        self.user_id = None
        self.datetime = None

    def set(self, user_id, datetime):
        self.user_id = str(user_id)
        timestamp = datetime / 1000  # convert timestamp from milliseconds to seconds
        datetime = dt.datetime.fromtimestamp(timestamp)
        self.datetime = f'{datetime:%Y-%m-%d_%H-%M-%S-%f}'

    def path(self, filename):
        p = self.data_dir / self.user_id / self.datetime
        p.mkdir(parents=True, exist_ok=True)
        return p / filename

    def save(self, filename, data):
        self.path(filename).write_text(data)
