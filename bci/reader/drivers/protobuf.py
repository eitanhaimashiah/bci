from ...protocol.utils.read import read_user, read_snapshot


class ProtobufDriver:
    """Represents a driver to read sample files of protobuf format.

    Attributes:
        format (str): Format of sample files this driver can handle.
        stream (IOBase): Stream representing the sample file.

    """

    format = 'protobuf'

    def __init__(self, stream):
        self.stream = stream

    def read_user(self):
        return read_user(self.stream)

    def read_snapshot(self):
        return read_snapshot(self.stream)
