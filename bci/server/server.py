import flask

from ..defaults import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT
from ..protocol.utils.parse_serialize import parse_from_message
from ..parsers import load_parsers, run_parser


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
    parsers = load_parsers()
    fields = list(parsers.keys())

    @app.route('/config', methods=['GET'])
    def get_config():
        try:
            return flask.jsonify({'fields': fields, 'error': None})
        except Exception as error:
            return flask.jsonify({'fields': None, 'error': str(error)}), 500

    @app.route('/snapshot', methods=['POST'])
    def post_snapshot():
        try:
            publish(parse_from_message(flask.request.data))
            return flask.jsonify({'error': None})
        except Exception as error:
            return flask.jsonify({'error': str(error)}), 500

    app.run(host=host, port=port, threaded=True, debug=True)
