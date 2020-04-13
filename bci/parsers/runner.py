import sys
import pathlib
import importlib
import inspect

modules = []
parsers = {}


def run_parser(topic, data):
    """Runs the parser named `name` on `data`.

    Args:
        topic (str): Parser name.
        data (bytes): Raw data, as consumed from the message queue.
            The data contains one snapshot alongside the user
            information.

    Returns:
        str: The parser result dumped as a JSON string.

    """
    # TODO Check this function again
    parsers[topic](data)

# TODO Organize the whole file

def load_modules():
    root = pathlib.Path(__file__).absolute().parent
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))


# load_modules(__file__)
#
#
# def load_parsers(module):
#     pass
#
#
# for module in modules:
#     load_parsers(module)

# def get_parsers():
#     modules = _load_modules()
#     parsers = {}
#     for module in modules:
#         for key, value in module.__dict__.items():
#             if key.startswith('parse_') and callable(value):
#                 parsers[value.field] = value
#             if key.endswith('Parser') and inspect.isclass(value):
#                 parsers[value.field] = value().__dict__['parse']
#     return parsers
#
#
# def _load_modules():
#     modules = []
#     root = pathlib.Path(__file__).absolute().parent
#     sys.path.insert(0, str(root.parent))
#     for path in root.iterdir():
#         if path.name.startswith('_') or not path.suffix == '.py':
#             continue
#         modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))
#     return modules
