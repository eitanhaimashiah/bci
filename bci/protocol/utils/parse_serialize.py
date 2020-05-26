import struct
import io

from .read import read_user, read_snapshot


def serialize_to_message(user, snapshot):
    """Serializes `user` and `snapshot` to a message.

    Args:
        user (bci.protocol.sample_pb2.User): User object.
        snapshot (bci.protocol.sample_pb2.Snapshot): Snapshot object.

    Returns:
        bytes: Message serializing `user` and `snapshot`.

    """
    user_data = user.SerializeToString()
    user_size = struct.pack('<I', len(user_data))
    snapshot_data = snapshot.SerializeToString()
    snapshot_size = struct.pack('<I', len(snapshot_data))
    return user_size + user_data + snapshot_size + snapshot_data


def parse_from_message(data):
    """Parses `data` to a tuple composed of User and Snapshot objects.

    Args:
        data (bytes): Binary data composed of a sequence of a message
            size (uint32) and a message of that size.

    Returns:
        tuple: Tuple containing:
            user (bci.protocol.sample_pb2.User): User object parsed from `data`.
            snapshot (bci.protocol.sample_pb2.Snapshot): Snapshot object parsed from `data`.

    """
    stream = io.BytesIO(data)
    user = read_user(stream)
    snapshot = read_snapshot(stream)
    return user, snapshot
