import struct
import gzip
import datetime as dt
from .protobuf.bci_pb2 import User, Snapshot


class Reader:
    def __init__(self, path):
        self.path = path

        # Open the sample file according to its extension
        if self.path.endswith('.gz'):
            self.fd = gzip.open(self.path, 'rb')
        else:
            self.fd = open(self.path, 'rb')

        self._read_user_info()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._read_snapshot()
        except Exception:
            self.fd.close()
            raise StopIteration

    def _read_message(self):
        message_size, = struct.unpack('<I', self.fd.read(4))
        message = self.fd.read(message_size)
        return message

    def _read_user_info(self):
        data = self._read_message()
        self.user = User()
        self.user.ParseFromString(data)

    def _read_snapshot(self):
        data = self._read_message()
        self.snapshot = Snapshot()
        self.snapshot.ParseFromString(data)
        return self.snapshot

    def print_user(self):
        if self.user.gender == User.MALE:
            gender = 'male'
        elif self.user.gender == User.FEMALE:
            gender = 'female'
        else:
            gender = 'other'
        birthday = dt.datetime.fromtimestamp(self.user.birthday)
        print(f'user {self.user.user_id}: {self.user.username} born {birthday:%B %-d, %Y} ({gender})')

    def print_snapshot(self):
        timestamp = self.snapshot.datetime / 1000  # convert timestamp from milliseconds to seconds
        datetime = dt.datetime.fromtimestamp(timestamp)
        trans = self.snapshot.pose.translation
        rot = self.snapshot.pose.rotation
        print(f'Snapshot from {datetime:%B %-d, %Y at %H:%M:%S.%f} '
              f'on ({trans.x:.2f}, {trans.y:.2f}, {trans.z:.2f}) / '
              f'({rot.x:.2f}, {rot.y:.2f}, {rot.z:.2f}, {rot.w:.2f}) '
              f'with a '
              f'{self.snapshot.color_image.width}x{self.snapshot.color_image.height} color image '
              f'and a '
              f'{self.snapshot.depth_image.width}x{self.snapshot.depth_image.height} depth image.')


def read(path):
    reader = Reader(path)
    reader.print_user()
    for _ in reader:
        reader.print_snapshot()
