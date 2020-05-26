import numpy as np

from .display import get_datetime_str

# TODO Maybe I should document this class


class Context:
    def __init__(self, root):
        self.root = root
        self.user_id = None
        self.snapshot_id = None

    def set(self, *, user=None, user_id=None,
            snapshot=None, snapshot_datetime=None):
        if user:
            assert not user_id, '`user` and `user_id` cannot be specified together'
            user_id = user.user_id
        if user_id:
            self.user_id = str(user_id)
        if snapshot:
            assert not snapshot_datetime, '`snapshot` and `snapshot_datetime` cannot be specified together'
            snapshot_datetime = snapshot.datetime
        if snapshot_datetime:
            assert snapshot_datetime, '`datetime` must be given'
            self.snapshot_id = get_datetime_str(snapshot_datetime,
                                                purpose='save')
            # self.snapshot_id = str(snapshot_datetime)

    def path(self, filename, is_raw=True):
        assert self.user_id
        path = self.root / self.user_id
        if self.snapshot_id:
            path /= self.snapshot_id
        if is_raw:
            path /= 'raw_data'
        else:
            path /= 'results'
        path.mkdir(parents=True, exist_ok=True)
        return path / filename

    def save(self, filename, data, is_binary=True, is_raw=True):
        path = self.path(filename, is_raw)
        if is_binary:
            path.write_bytes(data)
        else:
            path.write_text(data)
        return path

    def save_blobs(self, user, snapshot):
        self.set(user=user, snapshot=snapshot)
        color_image_path = self.save('color_image', snapshot.color_image.data)
        depth_image_path = self.path('depth_image.npy')  # TODO Understand how to drop the extention `npy`
        np.save(depth_image_path, snapshot.depth_image.data)
        return color_image_path, depth_image_path
