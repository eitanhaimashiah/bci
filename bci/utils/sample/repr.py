import datetime as dt
from .sample_pb2 import User


def user_repr(user):
    if user.gender == User.MALE:
        gender = 'male'
    elif user.gender == User.FEMALE:
        gender = 'female'
    else:
        gender = 'other'
    birthday = dt.datetime.fromtimestamp(user.birthday)
    return f'User {user.user_id}: {user.username}, ' \
           f'born {birthday:%B %-d, %Y} ({gender})'


def snapshot_repr(snapshot):
    timestamp = snapshot.datetime / 1000  # convert timestamp from milliseconds to seconds
    datetime = dt.datetime.fromtimestamp(timestamp)
    trans = snapshot.pose.translation
    rot = snapshot.pose.rotation
    return f'Snapshot from {datetime:%B %-d, %Y at %H:%M:%S.%f} ' \
           f'on ({trans.x:.2f}, {trans.y:.2f}, {trans.z:.2f}) / ' \
           f'({rot.x:.2f}, {rot.y:.2f}, {rot.z:.2f}, {rot.w:.2f}) ' \
           f'with a ' \
           f'{snapshot.color_image.width}x{snapshot.color_image.height} ' \
           f'color image and a ' \
           f'{snapshot.depth_image.width}x{snapshot.depth_image.height} ' \
           f'depth image.'
