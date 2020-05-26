import inspect

from ...utils.load import load_modules

modules = []


def find_driver(format):
    """Finds the driver corresponding to `format`.

    Args:
        format (str): Format of the sample file.

    Returns:
        The driver corresponding to `format`.

    Raises:
        ValueError: If `format` is unknown.

    """
    global modules
    if not modules:
        modules = load_modules(__file__)

    # Find the appropriate driver class for `format`
    for module in modules:
        for key, value in module.__dict__.items():
            if key.endswith('Driver') and inspect.isclass(value)\
                    and value.format == format:
                return value

    raise ValueError(f'unknown format: {format}')
