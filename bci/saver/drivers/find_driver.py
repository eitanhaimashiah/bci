import inspect

from ...utils.load import load_modules

modules = []


def find_driver(scheme):
    """Finds the driver corresponding to `scheme`.

    Args:
        scheme (str): The database scheme.

    Returns:
        The driver corresponding to `scheme`.

    Raises:
        ValueError: If `scheme` is unknown.

    """
    global modules
    if not modules:
        modules = load_modules(__file__)

    # Find the driver corresponding to `scheme`
    for module in modules:
        for key, value in module.__dict__.items():
            # TODO Change it because now the driver is in a subpackage
            if key.endswith('Driver') and inspect.isclass(value)\
                    and value.scheme == scheme:
                return value

    raise ValueError(f'unknown scheme: {scheme}')
