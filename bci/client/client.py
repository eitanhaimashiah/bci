import requests
from ..reader import Reader
from ..utils.sample.sample_pb2 import AssociatedSnapshot


def _clear_non_requested_fields(snapshot, requested_fields):
    all_fields = snapshot.DESCRIPTOR.fields_by_name.keys()
    non_requested_fields = set(all_fields) - set(requested_fields)
    for field in non_requested_fields:
        snapshot.ClearField(field)


def upload_sample(host, port, path, fmt='protobuf'):
    """Uploads snapshots from the specified path to the server sourced at `host:port`."""
    url = f'http://{host}:{port}'
    reader = Reader(path, fmt)
    associated_snapshot = AssociatedSnapshot()

    requested_fields = requests.get(f'{url}/config').json()['fields']
    for snapshot in reader:
        _clear_non_requested_fields(snapshot, requested_fields)
        associated_snapshot.user.CopyFrom(reader.user)
        associated_snapshot.snapshot.CopyFrom(snapshot)
        requests.post(f'{url}/snapshot', associated_snapshot.SerializeToString())
        print('sent')
    print('done')


