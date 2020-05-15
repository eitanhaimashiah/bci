import inspect

from ...utils.load import load_modules

modules = []


def find_driver(format, stream):
    """Finds the driver corresponding to `format`.

    Args:
        format (str): Format of the sample file.
        stream (IOBase): Stream representing the sample file.

    Returns:
        The driver object corresponding to `format`.

    Raises:
        ValueError: If `format` is not supported.

    """
    global modules

    if not modules:
        modules = load_modules(__file__)

    # Find the appropriate driver class for `format`
    for module in modules:
        for key, value in module.__dict__.items():
            if key.endswith('Driver') and inspect.isclass(value)\
                    and value.format == format:
                return value(stream)

    raise ValueError(f'unknown format: {format}')
