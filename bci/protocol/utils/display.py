import datetime as dt

from .. import sample_pb2 as sample


def display_user(user):
    """Displays `user` in a human-readable form.

    Args:
        user (bci.protocol.sample_pb2.User): User object.

    """
    gender = get_gender_str(user.gender)
    birthday = dt.datetime.fromtimestamp(user.birthday)
    # TODO Decomment following code when working on Windows. For some reason, datetime format doesn't work on Windows
    # print(f'User {user.user_id}: {user.username}, '
    #       f'born {birthday:%B %-d, %Y} ({gender})')
    print(f'User {user.user_id}: {user.username}, '
          f'born {birthday} ({gender})')


def display_snapshot(snapshot):
    """Displays `snapshot` in a human-readable form.

    Args:
        snapshot (bci.protocol.sample_pb2.Snapshot): Snapshot object.

    """
    datetime_str = get_datetime_str(snapshot.datetime)
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


def get_gender_str(user_gender):
    """Gets a string representation of the given user's gender field.

    Args:
        user_gender (typing.Union[int, str]): User's gender.

    Returns:
        str: The required string.

    Raises:
        ValueError: If `user_gender` is unknown.

    """
    try:
        if isinstance(user_gender, int):
            user_gender = sample.User.Gender.Name(user_gender)
        return user_gender.lower()
    except ValueError:
        raise ValueError(f'unknown gender: {user_gender}')


def get_datetime_str(snapshot_datetime, purpose='display'):
    """Gets a string representation of the given snapshot's datetime field.
    Args:
        snapshot_datetime (typing.Union[int, str])): Snapshot's datetime.
        purpose (str): For what purpose the result will be used.
            Default to 'display'.

    Returns:
        str: The required string according to `purpose`.

    Raises:
        ValueError: If `purpose` is unknown.

    """
    timestamp = int(snapshot_datetime) / 1000  # convert timestamp from milliseconds to seconds
    datetime = dt.datetime.fromtimestamp(timestamp)
    if purpose == 'display':
        # TODO Decomment following code when working on Windows. For some reason, datetime format doesn't work on Windows
        # return datetime.strftime('%B %-d, %Y at %H:%M:%S.%f')[:-3]
        return datetime
    elif purpose == 'save':
        return datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
    else:
        raise ValueError(f'unknown purpose: {purpose}')
