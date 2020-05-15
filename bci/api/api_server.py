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
    # TODO Complete
    pass
