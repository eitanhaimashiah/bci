import struct
import io

from .read import read_user, read_snapshot


def serialize_to_binary_tuple(message):
    """Serializes `message` to a binary consisting of the message
    size followed by the serialized message.

    Args:
        message (google.protobuf.message.Message): A message.

    Returns:
        bytes: The required bytes.

    """
    serialized_message = message.SerializeToString()
    message_size = struct.pack('<I', len(serialized_message))
    return message_size + serialized_message


def serialize_to_binary_seq(user, *snapshots):
    """Serializes `user` and `snapshots` to a binary with a sequence
    of message sizes and serialized messages (of that size), where
    the first one is `user`, and the rest are `snapshots`.

    Args:
        user (bci.protocol.sample_pb2.User): User message.
        snapshots (List[bci.protocol.sample_pb2.Snapshot]): List of
            Snapshot messages.

    Returns: The required bytes.

    """
    data = serialize_to_binary_tuple(user)
    for snapshot in snapshots:
        data += serialize_to_binary_tuple(snapshot)
    return data


def parse_from_binary_seq(data):
    """Parses `data` to a tuple composed of User and Snapshot messages.

    Args:
        data (bytes): A binary with a sequence of message sizes and
            serialized messages (of that size), where where the first
            one is a User message and the second is a Snapshot message.

    Returns:
        tuple: Tuple containing:
            user (bci.protocol.sample_pb2.User): User message parsed from `data`.
            snapshot (bci.protocol.sample_pb2.Snapshot): Snapshot message parsed from `data`.

    """
    stream = io.BytesIO(data)
    user = read_user(stream)
    snapshot = read_snapshot(stream)
    return user, snapshot
