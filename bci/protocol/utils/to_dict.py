import google.protobuf.json_format as pjf

from .display import get_gender_str
from .. import sample_pb2 as sample


def user_to_dict(user):
    """Converts `user` to a dictionary.

    Args:
        user (bci.protocol.sample_pb2.User): User object.

    Returns:
        dict: A dictionary representation of `user`.

    """
    user_dict = pjf.MessageToDict(user, preserving_proto_field_name=True)
    user_dict['gender'] = get_gender_str(user.gender)
    return user_dict


def snapshot_to_dict(snapshot, color_image_path, depth_image_path):
    """Converts `snapshot` to a dictionary.

    Args:
        snapshot (bci.protocol.sample_pb2.Snapshot): Snapshot object.
        color_image_path (str): Path to the binary data of the
            `snapshot`'s color image field.
        depth_image_path (str): Path to the binary data of the
            `snapshot`'s depth image field.

    Returns:
        dict: A dictionary representation of `snapshot`, where images'
        binary data substituted by the paths in which they were saved.

    """
    snapshot_metadata = sample.Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = pjf.MessageToDict(snapshot_metadata,
                                      preserving_proto_field_name=True,
                                      including_default_value_fields=True)
    snapshot_dict['color_image']['data'] = color_image_path
    snapshot_dict['depth_image']['data'] = depth_image_path
    return snapshot_dict
