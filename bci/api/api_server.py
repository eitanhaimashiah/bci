import furl
import flask
import flask_cors as fc

from ..defaults import DEFAULT_API_SERVER_HOST, \
    DEFAULT_API_SERVER_PORT, DEFAULT_DB_URL
from ..saver.drivers import find_driver


def run_api_server(host=None, port=None, database_url=None):
    """Listens on `host:port` and serves data from `database_url`.

    Args:
        host (:obj:`str`, optional): API server's IP address. Default
            to `DEFAULT_API_SERVER_HOST`.
        port (:obj:`int`, optional): API server's port. Default to
            `DEFAULT_API_SERVER_PORT`.
        database_url (:obj:`str`, optional): URL of the running
            database. Default to `DEFAULT_DB_URL`

    """
    host = host or DEFAULT_API_SERVER_HOST
    port = port or DEFAULT_API_SERVER_PORT
    database_url = database_url or DEFAULT_DB_URL
    app = flask.Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    fc.CORS(app, resources={'/': {'origins': f'http://{host}:{port}'}})
    driver_cls = find_driver(furl.furl(database_url).scheme)
    driver = driver_cls(database_url, setup=False)

    @app.route('/users', methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_users():
        return flask.jsonify({'users': driver.get('users')})

    @app.route('/users/<user_id>', methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_user(user_id):
        return flask.jsonify(driver.get('user', user_id=user_id))

    @app.route('/users/<user_id>/snapshots', methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_snapshots(user_id):
        snapshots = driver.get('snapshots', user_id=user_id)
        return flask.jsonify({'snapshots': snapshots})

    @app.route('/users/<user_id>/snapshots/<snapshot_id>',
               methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_snapshot(user_id, snapshot_id):
        snapshot = driver.get('snapshot',
                              user_id=user_id,
                              snapshot_id=snapshot_id)
        return flask.jsonify(snapshot)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>',
               methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_result(user_id, snapshot_id, result_name):
        if result_name in ['color_image', 'depth_image']:
            result = {
                'link': flask.request.base_url + '/data'
            }
        else:
            result = driver.get('result',
                                result_name=result_name,
                                snapshot_id=snapshot_id)
        return flask.jsonify(result)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data',
               methods=['GET'])
    @fc.cross_origin(origin=f'{host}',
                     headers=['Content-Type', 'Authorization'])
    def get_result_data(user_id, snapshot_id, result_name):
        assert result_name in ['color_image', 'depth_image']
        result = driver.get('result',
                            result_name=result_name,
                            snapshot_id=snapshot_id)
        return flask.send_file(result['path'],
                               mimetype='image/jpg')

    app.run(host=host, port=port, threaded=True)
