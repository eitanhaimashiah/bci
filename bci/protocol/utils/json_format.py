import json
import pathlib
import google.protobuf.json_format as pbj

from .display import get_gender_str
from .. import sample_pb2 as pb


def json_user(user):
    """Serializes `user` to a JSON formatted string.

    Args:
        user (pb.User): User object.

    Returns:
        str: String serializing `user` in JSON format.

    """
    user_dict = pbj.MessageToDict(user, preserving_proto_field_name=True)
    user_dict['gender'] = get_gender_str(user)
    return json.dumps(user_dict)


def json_snapshot(snapshot, user_id, blobs_path):
    """Serializes `snapshot` to a JSON formatted string.

    Args:
        snapshot (pb.Snapshot): Snapshot object.
        user_id (int): User ID corresponding the `snapshot`.
        blobs_path (str): Path to the binary data.

    Returns:
        str: String serializing `snapshot` in JSON format, while binary
        data substituted by the path in which it saved.

    """
    blobs_path = pathlib.Path(blobs_path)
    snapshot_metadata = pb.Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = pbj.MessageToDict(snapshot_metadata,
                                      preserving_proto_field_name=True,
                                      including_default_value_fields=True)
    snapshot_dict['user_id'] = user_id
    snapshot_dict['color_image']['data'] = str(blobs_path / 'color_image')
    snapshot_dict['depth_image']['data'] = str(blobs_path / 'depth_image.npy')
    return json.dumps(snapshot_dict)
