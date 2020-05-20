import datetime as dt

from .. import sample


def display_user(user):
    """Displays `user` in a human-readable form.

    Args:
        user (bci.protocol.sample.User): User object.

    """
    gender = get_gender_str(user)
    birthday = dt.datetime.fromtimestamp(user.birthday)
    print(f'User {user.user_id}: {user.username}, '
          f'born {birthday:%B %-d, %Y} ({gender})')


def display_snapshot(snapshot):
    """Displays `snapshot` in a human-readable form.

    Args:
        snapshot (bci.protocol.sample.Snapshot): Snapshot object.

    """
    datetime_str = get_datetime_str(snapshot)
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


def get_gender_str(user):
    """Gets a string representation of the `gender` field in the
    given user.

    Args:
        user (bci.protocol.sample.User): User object.

    Returns:
        str: The required string.

    """
    if user.gender == sample.User.MALE:
        return 'male'
    elif user.gender == sample.User.FEMALE:
        return 'female'
    else:
        return 'other'


def get_datetime_str(snapshot, purpose='display'):
    """Gets a string representation of the `datetime` field in the
    given snapshot.

    Args:
        snapshot (bci.protocol.sample.Snapshot): Snapshot object.
        purpose (str): For what purpose the result will be used.
            Default to 'display'.

    Returns:
        str: The required string according to `purpose`.

    Raises:
        ValueError: If `purpose` is not supported.

    """
    timestamp = snapshot.datetime / 1000  # convert timestamp from milliseconds to seconds
    datetime = dt.datetime.fromtimestamp(timestamp)
    if purpose == 'display':
        return datetime.strftime('%B %-d, %Y at %H:%M:%S.%f')[:-3]
    elif purpose == 'save':
        return datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
    else:
        raise ValueError(f'unknown purpose: {purpose}')
