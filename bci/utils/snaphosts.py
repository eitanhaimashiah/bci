import struct
from io import BytesIO


def create_stream(user, snapshots):
    user_data = user.SerializeToString()
    user_size = struct.pack('<I', len(user_data))

    data = user_size + user_data

    for snapshot in snapshots:
        snapshot_data = snapshot.SerializeToString()
        snapshot_size = struct.pack('<I', len(snapshot_data))

        data += snapshot_size + snapshot_data

    return BytesIO(data)
