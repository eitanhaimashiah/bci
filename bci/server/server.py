import flask
import json

from ..defaults import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT, BLOBS_DIR
from ..protocol.utils import Context
from ..protocol.utils.display import display_snapshot
from ..protocol.utils.parse_serialize import parse_from_binary_seq
from ..protocol.utils.to_dict import user_to_dict, snapshot_to_dict
from ..parsers import get_fields


def run_server(publish, host=None, port=None):
    """Listens on `host:port` and passes received messages to `publish`.

    Args:
        publish (function): Publishing function.
        host (:obj:`str`, optional): Server's IP address. Default to
            `DEFAULT_SERVER_HOST`.
        port (:obj:`int`, optional): Server's port. Default to
            `DEFAULT_SERVER_PORT`.

    Raises:
        TODO Complete (can't find flask errors)

    """
    host = host or DEFAULT_SERVER_HOST
    port = port or DEFAULT_SERVER_PORT
    app = flask.Flask(__name__)
    fields = get_fields()

    @app.route('/config', methods=['GET'])
    def get_config():
        try:
            return flask.jsonify({'fields': fields, 'error': None})
        except Exception as error:
            return flask.jsonify({'fields': None, 'error': str(error)}), 500

    @app.route('/snapshot', methods=['POST'])
    def post_snapshot():
        try:
            user, snapshot = parse_from_binary_seq(flask.request.data)
            display_snapshot(snapshot)
            color_image_path, depth_image_path = Context(BLOBS_DIR).save_blobs(user, snapshot)
            publish(json.dumps({
                'user': user_to_dict(user),
                'snapshot': snapshot_to_dict(snapshot,
                                             color_image_path=str(color_image_path),
                                             depth_image_path=str(depth_image_path))
            }))
            return flask.jsonify({'error': None})
        except Exception as error:
            # TODO Replace this code with the `bci.utils.cli`'s traceback handling
            import os
            import traceback
            print(os.linesep + traceback.format_exc().strip())
            return flask.jsonify({'error': str(error)}), 500

    app.run(host=host, port=port, threaded=True)
