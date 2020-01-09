import pathlib


_ROOT = pathlib.Path(__file__).absolute().parent.parent.parent
_SNAPSHOT_DIR = _ROOT / 'snapshots'


class Context:
    def __init__(self, snapshot_dir=_SNAPSHOT_DIR):
        self.snapshot_dir = snapshot_dir

    def path(self, filename):
        return self.snapshot_dir / filename

    def save(self, filename, data):
        self.path(filename).write_text(data)
