import inspect
import furl

from ...utils.load import load_modules

modules = []


def find_driver(url):
    """Finds the driver corresponding to `url`'s scheme.

    Args:
        url (str): URL of the message queue's server.

    Returns:
        The driver object corresponding to `url`'s scheme.

    Raises:
        ValueError: If `url`'s scheme is not supported.

    """
    global modules

    if not modules:
        modules = load_modules(__file__)

    # Find the publisher corresponding to `scheme`
    scheme = furl.furl(url).scheme
    for module in modules:
        for key, value in module.__dict__.items():
            if key.endswith('Publisher') and inspect.isclass(value)\
                    and value.scheme == scheme:
                return value(url)

    raise ValueError(f'unknown scheme: {format}')
