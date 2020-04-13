from flask import Flask, request
from ..protocol.sample_pb2 import AssociatedSnapshot
from ..defaults import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT


def _flatten(l):
    gather = []
    for item in l:
        if isinstance(item, tuple):
            gather.extend(item)
        else:
            gather.append(item)
    return gather


def run_server(publish, host=None, port=None):
    """Listens on `host:port` and passes received messages to `publish`.

    Args:
        publish (function): Publishing function.
        host (:obj:`str`, optional): Server's IP address. Default to
            `DEFAULT_SERVER_IP`.
        port (:obj:`int`, optional): Server's port. Default to
            `DEFAULT_SERVER_PORT`.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        TODO Complete

    """
    # TODO Check this function again
    host = host or DEFAULT_SERVER_IP
    port = port or DEFAULT_SERVER_PORT
    app = Flask(__name__)
    fields = ['color_image', 'depth_image', 'feelings', 'pose']  # TODO Change it to the appropriate function

    @app.route('/config', methods=['GET'])
    def get_config():
        return {'fields': fields}

    @app.route('/snapshot', methods=['POST'])
    def post_snapshot():
        user_snapshot = AssociatedSnapshot()
        user_snapshot.ParseFromString(request.data)
        publish(user_snapshot)
        return {}

    app.run(host=host, port=port, threaded=True, debug=True)
