import requests
from ..reader import Reader
from ..protocol.sample_pb2 import Snapshot
from ..protocol.utils.parse_serialize import serialize_to_message
from ..protocol.utils.display import get_datetime_str
from ..defaults import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT


def upload_sample(path, host=None, port=None, format=None):
    """Reads the sample file from `path` and uploads it to the server
    listening on `host:port`.

    Args:
        path (str): Path of the sample file.
        host (:obj:`str`, optional): Server's IP address. Default to
            `DEFAULT_SERVER_HOST`.
        port (:obj:`int`, optional): Server's port. Default to
            `DEFAULT_SERVER_PORT`.
        format (:obj:`str`, optional): Format of the sample file.
            Default to `DEFAULT_FORMAT`

    Raises:
        ValueError: If `format` is not supported.
        OSError: If a failure occurs while reading the sample file.
        requests.exceptions.RequestException: If there was an
            ambiguous exception that occurred while communicating with
            the server.

    """
    host = host or DEFAULT_SERVER_HOST
    port = port or DEFAULT_SERVER_PORT
    url = f'http://{host}:{port}'
    reader = Reader(path, format)
    config = requests.get(f'{url}/config').json()['fields']
    for snapshot in reader:
        fields = {field: getattr(snapshot, field) for field in config}
        snapshot = Snapshot(datetime=snapshot.datetime, **fields)
        requests.post(f'{url}/snapshot',
                      serialize_to_message(reader.user, snapshot))
        print(f'Sent the snapshot from {get_datetime_str(snapshot)}')
    print('Done')
