import struct
import gzip
from ...utils.sample.sample_pb2 import User, Snapshot


class ProtobufDriver:
    def __init__(self, path):
        self.file = gzip.open(path, 'rb')

    def close_file(self):
        self.file.close()

    def read_user(self):
        data = self._read_message()
        user = User()
        user.ParseFromString(data)
        return user

    def read_snapshot(self):
        data = self._read_message()
        snapshot = Snapshot()
        snapshot.ParseFromString(data)
        return snapshot

    def _read_message(self):
        size, = struct.unpack('<I', self.file.read(
            struct.calcsize('<I')))
        message = self.file.read(size)
        return message
