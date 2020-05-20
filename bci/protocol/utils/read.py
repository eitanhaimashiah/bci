from .. import sample_pb2 as sample
from ...utils.struct import read_struct_by_format


def read_user(stream):
    """Read a User object from `stream`.

    Args:
        stream (IOBase): Stream we are reading from.

    Returns:
        bci.protocol.sample.User: The User object read from `stream`.

    """
    data = read_message(stream)
    user = sample.User()
    user.ParseFromString(data)
    return user


def read_snapshot(stream):
    """Read a Snapshot object from `stream`.

    Args:
        stream (IOBase): Stream we are reading from.

    Returns:
        bci.protocol.sample.Snapshot: The Snapshot object read from `stream`.

    """
    data = read_message(stream)
    snapshot = sample.Snapshot()
    snapshot.ParseFromString(data)
    return snapshot


def read_message(stream):
    """Reads binary data composed of a sequence of a message size
    (uint32) and a message of that size.

    Args:
        stream (IOBase): Stream we are reading from.

    Returns:
        bytes: The message as a bytes object.

    """
    size, = read_struct_by_format(stream, '<I')
    message = stream.read(size)
    return message
