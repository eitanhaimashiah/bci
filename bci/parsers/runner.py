import inspect
import json

from ..defaults import BLOBS_DIR
from ..protocol.utils import Context
from ..utils.load import load_modules

modules = []
parsers = {}
context = None


def load_parsers():
    """Imports all submodules of parsers, and creates a dictionary
    mapping a parser's field to its function or class.

    Returns:
        dict: A dictionary mapping a parser's field to its function
        or class.

    """
    global modules, parsers

    if not modules:
        modules = load_modules(__file__)

    # Map each parser's field to its function or class
    if not parsers:
        for module in modules:
            for key, value in module.__dict__.items():
                if key.startswith('parse_') and inspect.isfunction(value):
                    parsers[value.field] = value
                if key.endswith('Parser') and inspect.isclass(value):
                    parsers[value.field] = value()

    return parsers


def get_fields():
    """Gets the available parser names"""
    global parsers
    load_parsers()
    return list(parsers.keys())


def parse(field, data):  # TODO Consider replacing `field` with `topic`
    """Parses `data` on `field`.

    Args:
        field (str): Snapshot field to parse.
        data (str): JSON-formatted raw data, as consumed from the
            message queue. The data contains one snapshot alongside
            the user information.

    Returns:
        str: The parser result dumped as a JSON-formatted string.

    """
    global parsers, context
    load_parsers()
    if not context:
        context = Context(BLOBS_DIR)
    data = json.loads(data)
    user, snapshot = data['user'], data['snapshot']
    context.set(user_id=user['user_id'],
                snapshot_datetime=snapshot['datetime'])
    result = parsers[field](context, snapshot)
    return json.dumps({
        'user': user,
        'snapshot': {
            'snapshot_id': snapshot['datetime'],
            'datetime': snapshot['datetime']
        },
        'result': result
    })
