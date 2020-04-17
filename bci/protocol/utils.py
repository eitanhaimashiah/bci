import struct
import io
import datetime as dt
from . import sample_pb2 as pb


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


# def deserialize_user(data):
#     """Deserializes `data` to a User message object.
#
#     Args:
#         data (bytes): Binary data composed of a sequence of a user
#             message size (uint32) and a user message of that size.
#
#     Returns:
#         pb.User: User message object deserialized from `data`.
#
#     """
#     stream = io.BytesIO(data)
#     user_size, = struct.unpack('<I', stream.read(4))
#     user = bubbles_proto.User()
#     user.ParseFromString(stream.read(user_size))
#
#     snapshot_size, = struct.unpack('<I', stream.read(4))
#     snapshot = bubbles_proto.Snapshot()
#     snapshot.ParseFromString(stream.read(snapshot_size))
#
#     return user, snapshot
#
#
# def deserialize_message(data):
#     """Deserializes `data`.
#
#     Args:
#         data (bytes): Binary data composed of a sequence of a message
#             size (uint32) and a message of that size.
#
#     Returns:
#         (pb.User, pb.Snapshot): User and snapshot objects
#         deserialized from `data`.
#
#     """
#     stream = io.BytesIO(data)
#     user_size, = struct.unpack('<I', stream.read(4))
#     user = bubbles_proto.User()
#     user.ParseFromString(stream.read(user_size))
#
#     snapshot_size, = struct.unpack('<I', stream.read(4))
#     snapshot = bubbles_proto.Snapshot()
#     snapshot.ParseFromString(stream.read(snapshot_size))
#
#     return user, snapshot
#
#
# def serialize_message(user, snapshot):
#     '''Serialize user and snapshot objects to message.
#
#     :param user: user object.
#     :param snapshot: snapshot object.
#     :returns: message encodes the above objects.
#     :rtype: bytes
#     '''
#     user_data = user.SerializeToString()
#     user_size = struct.pack('<I', len(user_data))
#
#     snapshot_data = snapshot.SerializeToString()
#     snapshot_size = struct.pack('<I', len(snapshot_data))
#     return user_size + user_data + snapshot_size + snapshot_data
