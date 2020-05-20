import pathlib
import google.protobuf.json_format as pjf

from .display import get_gender_str
from .. import sample_pb2 as sample
from ...defaults import BLOBS_DIR


def user_to_dict(user):
    """Converts `user` to a dictionary.

    Args:
        user (bci.protocol.sample.User): User object.

    Returns:
        dict: A dict representation of `user`.

    """
    user_dict = pjf.MessageToDict(user, preserving_proto_field_name=True)
    user_dict['gender'] = get_gender_str(user)
    return user_dict


def snapshot_to_dict(snapshot):
    """Converts `snapshot` to a dictionary.

    Args:
        snapshot (bci.protocol.sample.Snapshot): Snapshot object.

    Returns:
        dict: A dict representation of `snapshot`, while binary data
        substituted by the path in which it saved.

    """
    snapshot_metadata = sample.Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = pjf.MessageToDict(snapshot_metadata,
                                      preserving_proto_field_name=True,
                                      including_default_value_fields=True)
    snapshot_dict['color_image']['data'] = str(BLOBS_DIR / 'color_image')
    snapshot_dict['depth_image']['data'] = str(BLOBS_DIR / 'depth_image.npy')
    return snapshot_dict
