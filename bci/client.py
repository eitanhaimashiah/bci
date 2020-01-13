import requests
from bci.reader import Reader
from .protobuf.bci_pb2 import UserAndSnapshot


def _clear_non_requested_fields(snapshot, requested_fields):
    non_requested_fields = set(['pose', 'feelings', 'color_image', 'depth_image']) - set(requested_fields)
    for field in non_requested_fields:
        snapshot.ClearField(field)


def upload_snapshots(address, path):
    """Uploads snapshots from the specified path to the server sourced at `address`."""
    host, port = address
    url = f'http://{host}:{port}'
    reader = Reader(path)
    user_snapshot = UserAndSnapshot()

    requested_fields = requests.get(f'{url}/config').json()['fields']
    for snapshot in reader:
        _clear_non_requested_fields(snapshot, requested_fields)
        user_snapshot.user.CopyFrom(reader.user)
        user_snapshot.snapshot.CopyFrom(snapshot)
        requests.post(f'{url}/snapshot', user_snapshot.SerializeToString())
        print('sent')
    print('done')
