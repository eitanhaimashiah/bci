import numpy as np

from .display import get_datetime_str


class Context:
    def __init__(self, root):
        self.root = root
        self.user_id = None
        self.snapshot_id = None

    def set(self, *, user=None, snapshot=None):
        if user:
            self.user_id = str(user.user_id)
        if snapshot:
            # self.snapshot_id = get_datetime_str(snapshot, purpose='save')
            self.snapshot_id = str(snapshot.datetime)

    def path(self, filename):
        assert self.user_id
        path = self.root / self.user_id
        if self.snapshot_id:
            path = path / self.snapshot_id
        path.mkdir(parents=True, exist_ok=True)
        return path / filename

    def save(self, filename, data):
        self.path(filename).write_text(data)

    def save_blobs(self, user, snapshot):
        self.set(user=user, snapshot=snapshot)
        self.path('color_image').write_bytes(snapshot.color_image.data)
        np.save(self.path('depth_image'), snapshot.depth_image.data)
