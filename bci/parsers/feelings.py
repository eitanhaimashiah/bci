def parse_feelings(context, snapshot):
    """Collects the feelings the user was experiencing at a given
    timestamp from `snapshot`.

    Args:
        context (bci.protocol.utils.Context): Context in the application.
        snapshot (dict): Snapshot as consumed from the message queue
            and converted to dictionary representation.

    Returns:
        dict: A dictionary containing `snapshot`'s feeling field.

    """
    return snapshot['feelings']


parse_feelings.field = 'feelings'
