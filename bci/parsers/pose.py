def parse_pose(context, snapshot):
    """Collects the translation and the rotation of the user's head
    at a given timestamp from `snapshot`.

    Args:
        context (bci.protocol.utils.Context): Context in the application.
        snapshot (dict): Snapshot as consumed from the message queue
            and converted to dictionary representation.

    Returns:
        dict: A dictionary containing `snapshot`'s translation and
        rotation fields.

    """
    return snapshot['pose']


parse_pose.field = 'pose'
