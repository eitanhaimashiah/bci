import flask
import pathlib
import os
import json

from ..defaults import DEFAULT_API_SERVER_HOST, DEFAULT_API_SERVER_PORT, DEFAULT_DATABASE


def run_api_server(host=None, port=None, database_url=None):
    """Listens on `host:port` and serves data from `database_url`.

    Args:
        host (:obj:`str`, optional): API server's IP address. Default
            to `DEFAULT_API_SERVER_HOST`.
        port (:obj:`int`, optional): API server's port. Default to
            `DEFAULT_API_SERVER_PORT`.
        database_url (:obj:`str`, optional): URL of the running
            database. Default to `DEFAULT_DATABASE`

    """
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    database_url = database_url or DEFAULT_DATABASE
    app = flask.Flask(__name__)

    # TODO Replace this hardcoded data loading with DB loading
    root = pathlib.Path(__name__).absolute().parent.parent
    data_dir = root / 'data'

    # TODO Handle errors in the GET requests

    @app.route('/users', methods=['GET'])
    def get_users():
        users = os.listdir(data_dir)
        return flask.jsonify({'users': users})

    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        user_dir = data_dir / user_id
        with open(user_dir / 'metadata.json') as f:
            metadata = json.load(f)
            return flask.jsonify(metadata)

    @app.route('/users/<user_id>/snapshots', methods=['GET'])
    def get_snapshots(user_id):
        user_dir = data_dir / user_id
        snapshots = [x.name for x in user_dir.iterdir() if x.is_dir()]
        return flask.jsonify({'snapshots': snapshots})

    @app.route('/users/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
    def get_snapshot(user_id, snapshot_id):
        snapshot_dir = data_dir / user_id / snapshot_id
        with open(snapshot_dir / 'metadata.json') as f:
            metadata = json.load(f)
            return flask.jsonify(metadata)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
    def get_result(user_id, snapshot_id, result_name):
        snapshot_dir = data_dir / user_id / snapshot_id
        with open(snapshot_dir / f'{result_name}.json') as f:
            metadata = json.load(f)
            return flask.jsonify(metadata)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data', methods=['GET'])
    def get_result_data(user_id, snapshot_id, result_name):
        snapshot_dir = data_dir / user_id / snapshot_id
        return flask.send_file(snapshot_dir / f'{result_name}_data.jpg',
                               mimetype='image/jpg')

    app.run(host=host, port=port, threaded=True, debug=True)
