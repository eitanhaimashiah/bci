import struct
import io
import datetime as dt

from . import sample_pb2 as pb
from ..utils.struct import read_struct_by_format


# Displaying

def display_user(user):
    """Displays `user` in a human-readable form.

    Args:
        user (pb.User): User object.

    """
    if user.gender == pb.User.MALE:
        gender = 'male'
    elif user.gender == pb.User.FEMALE:
        gender = 'female'
    else:
        gender = 'other'
    birthday = dt.datetime.fromtimestamp(user.birthday)
    print(f'User {user.user_id}: {user.username}, '
          f'born {birthday:%B %-d, %Y} ({gender})')


def display_snapshot(snapshot):
    """Displays `snapshot` in a human-readable form.

    Args:
        snapshot (pb.Snapshot): Snapshot object.

    """
    timestamp = snapshot.datetime / 1000  # convert timestamp from milliseconds to seconds
    datetime = dt.datetime.fromtimestamp(timestamp)
    datetime_str = datetime.strftime('%B %-d, %Y at %H:%M:%S.%f')[:-3]
    trans = snapshot.pose.translation
    rot = snapshot.pose.rotation
    print(f'Snapshot from {datetime_str} '
          f'on ({trans.x:.2f}, {trans.y:.2f}, {trans.z:.2f}) / '
          f'({rot.x:.2f}, {rot.y:.2f}, {rot.z:.2f}, {rot.w:.2f}) '
          f'with a '
          f'{snapshot.color_image.width}x{snapshot.color_image.height} '
          f'color image and a '
          f'{snapshot.depth_image.width}x{snapshot.depth_image.height} '
          f'depth image.')


# Reading

def read_user(stream):
    """Read a User object from `stream`.

    Args:
        stream (IOBase): Stream we are reading from.

    Returns:
        pb.User: The User object read from `stream`.

    """
    data = read_message(stream)
    user = pb.User()
    user.ParseFromString(data)
    return user


def read_snapshot(stream):
    """Read a Snapshot object from `stream`.

    Args:
        stream (IOBase): Stream we are reading from.

    Returns:
        pb.Snapshot: The Snapshot object read from `stream`.

    """
    data = read_message(stream)
    snapshot = pb.Snapshot()
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


# Parsing and Serialization

def serialize_to_message(user, snapshot):
    """Serializes `user` and `snapshot` to a message.

    Args:
        user (pb.User): User object.
        snapshot (pb.Snapshot): Snapshot object.

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
        (pb.User, pb.Snapshot): User and Snapshot objects parsed
        from `data`.

    """
    stream = io.BytesIO(data)
    user = read_user(stream)
    snapshot = read_snapshot(stream)
    return user, snapshot
