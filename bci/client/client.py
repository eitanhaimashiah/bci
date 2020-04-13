import requests
from .reader import Reader
from ..protocol.sample_pb2 import Snapshot, AssociatedSnapshot
from ..defaults import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, DEFAULT_FORMAT


def upload_sample(path, host=None, port=None, format=None):
    """Reads the sample file from `path` and uploads it to the server
    listening on `host:port`.

    Args:
        path (str): Path of the sample file.
        host (:obj:`str`, optional): Server's IP address. Default to
            `DEFAULT_SERVER_IP`.
        port (:obj:`int`, optional): Server's port. Default to
            `DEFAULT_SERVER_PORT`.
        format (:obj:`str`, optional): Format of the sample file.
            Default to `DEFAULT_FORMAT`

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        TODO Complete

    """
    # TODO Check this function again
    host = host or DEFAULT_SERVER_IP
    port = port or DEFAULT_SERVER_PORT
    format = format or DEFAULT_FORMAT
    url = f'http://{host}:{port}'
    reader = Reader(path, format)
    config = requests.get(f'{url}/config').json()['fields']
    for snapshot in reader:
        fields = {field: getattr(snapshot, field) for field in config}
        snapshot = Snapshot(datetime=snapshot.datetime, **fields)
        associated_snapshot = AssociatedSnapshot(user=reader.user, snapshot=snapshot)
        requests.post(f'{url}/snapshot', associated_snapshot.SerializeToString())
        print('sent')
    print('done')
    return True


