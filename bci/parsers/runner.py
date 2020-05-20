import inspect

from ..utils.load import load_modules

modules = []
parsers = {}


def load_parsers():
    """Imports all submodules of parsers, and creates a dictionary
    mapping a parser's field to its function or class.

    Returns:
        dict: A dictionary mapping a parser's field to its
        function or class.

    """
    global modules, parsers

    if not modules:
        modules = load_modules(__file__)

    # Map each parser's field to its function or class
    if not parsers:
        for module in modules:
            for key, value in module.__dict__.items():
                if key.startswith('parse') and inspect.isfunction(value):
                    parsers[value.field] = value
                if key.endswith('Parser') and inspect.isclass(value):
                    parsers[value.field] = value()

    return parsers


def run_parser(topic, context, data):
    """Runs the parser named `name` on `data`.

    Args:
        # parsers (dict): The dictionary mapping a parser's field to its
        #     function or class. Returned by the `load_parsers` function.
        topic (str): Parser name.
        context (Context): Context in the application.
        data (bytes): Raw data, as consumed from the message queue.
            The data contains one snapshot alongside the user
            information.

    Returns:
        str: The parser result dumped as a JSON string.

    """
    # TODO Check this function again
    global parsers
    parsers[topic](context, data)
