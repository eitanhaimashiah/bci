import pathlib


# CLI Defaults
DEFAULT_QUIET = False
DEFAULT_TRACEBACK = False

# Reader Defaults
DEFAULT_FORMAT = 'protobuf'

# Server Defaults
DEFAULT_SERVER_HOST = '0.0.0.0'
DEFAULT_SERVER_ACTUAL_HOST = '127.0.0.1'
DEFAULT_SERVER_PORT = 8000

# RabbitMQ Server Defaults
DEFAULT_RABBITMQ_SERVER_HOST = '0.0.0.0'
DEFAULT_RABBITMQ_SERVER_ACTUAL_HOST = '127.0.0.1'
DEFAULT_RABBITMQ_SERVER_PORT = 5672

# Publisher Defaults
DEFAULT_MQ_URL = f'rabbitmq://{DEFAULT_RABBITMQ_SERVER_HOST}:' \
              f'{DEFAULT_RABBITMQ_SERVER_PORT}/'
DEFAULT_IS_SUBSCRIBER = False

# PostgreSQL Server Defaults
DEFAULT_POSTGRESQL_SERVER_HOST = '0.0.0.0'
DEFAULT_POSTGRESQL_SERVER_ACTUAL_HOST = '127.0.0.1'
DEFAULT_POSTGRESQL_SERVER_PORT = 5432
DEFAULT_POSTGRESQL_SERVER_USER = 'bci'
DEFAULT_POSTGRESQL_SERVER_PASSWORD = 'pass'


# Saver Defaults
DEFAULT_DB_URL = f'postgresql://{DEFAULT_POSTGRESQL_SERVER_USER}' \
                 f':{DEFAULT_POSTGRESQL_SERVER_PASSWORD}' \
                 f'@{DEFAULT_POSTGRESQL_SERVER_HOST}' \
                 f':{DEFAULT_POSTGRESQL_SERVER_PORT}'
DEFAULT_SETUP = True
DEFAULT_STR_DATES = True

# API Server Defaults
DEFAULT_API_SERVER_HOST = '0.0.0.0'
DEFAULT_API_SERVER_ACTUAL_HOST = '127.0.0.1'
DEFAULT_API_SERVER_PORT = 5000

# Web Server Defaults
DEFAULT_WEB_SERVER_HOST = '0.0.0.0'
DEFAULT_WEB_SERVER_ACTUAL_HOST = '127.0.0.1'
DEFAULT_WEB_SERVER_PORT = 8080

# Shared Filesystem
# TODO Uncomment the next line and comment the line following it
FS_ROOT = pathlib.Path('/tmp/bcifs')    # Root directory of the shared FS
# FS_ROOT = pathlib.Path(__file__).absolute().parent.parent
BLOBS_DIR = FS_ROOT / 'blobs'           # Directory of the binary data
DATA_DIR = FS_ROOT / 'data'

# Requests Defaults
OK_STATUS_CODE = 200
