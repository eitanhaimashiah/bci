import os
import pathlib
from datetime import datetime
from flask import Flask, render_template

from ..defaults import DEFAULT_WEB_SERVER_IP, DEFAULT_WEB_SERVER_PORT, \
    DEFAULT_API_SERVER_HOST, DEFAULT_API_SERVER_PORT, DATA_DIR


def run_server(host=None, port=None, api_host=None, api_port=None):
    """Listens on `host:port`, consumes the API and reflects it.

    Args:
        host (:obj:`str`, optional): Web server's IP address. Default
            to `DEFAULT_WEB_SERVER_IP`.
        port (:obj:`int`, optional): Web server's port. Default to
            `DEFAULT_WEB_SERVER_PORT`.
        api_host (:obj:`str`, optional): API server's IP address.
            Default to `DEFAULT_API_SERVER_HOST`.
        api_port (:obj:`int`, optional): API server's port. Default to
            `DEFAULT_API_SERVER_PORT`.


    Returns:
        bool: True if successful, False otherwise.

    Raises:
        TODO Complete

    """
    # TODO Update this function and exclude `data_dir`
    host = host or DEFAULT_WEB_SERVER_IP
    port = port or DEFAULT_WEB_SERVER_PORT
    api_host = api_host or DEFAULT_API_SERVER_HOST
    api_port = api_port or DEFAULT_API_SERVER_PORT
    app = Flask(__name__,
                static_folder='app/build/static',
                template_folder='app/build')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        """Serves the React app. All routes are routed to the react app.

        Args:
            path (str): Path browsed.

        """
        api_root = f'http://{api_host}:{api_port}'
        return render_template('index.html', api_root=api_root)

    app.run(host=host, port=port)
