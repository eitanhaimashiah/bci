from ...protocol import sample_pb2 as pb
from ...utils.struct import read_by_format


class ProtobufDriver:
    """Represents a driver to read sample files of protobuf format.

    Attributes:
        stream (IOBase): Stream representing the sample file.

    """

    def __init__(self, stream):
        self.stream = stream

    def read_user(self):
        data = self._read_message()
        user = pb.User()
        user.ParseFromString(data)
        return user

    def read_snapshot(self):
        data = self._read_message()
        snapshot = pb.Snapshot()
        snapshot.ParseFromString(data)
        return snapshot

    def _read_message(self):
        size, = read_by_format(self.stream, '<I')
        message = self.stream.read(size)
        return message
