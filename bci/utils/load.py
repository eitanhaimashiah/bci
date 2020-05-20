import sys
import pathlib
import importlib


def load_modules(loader_file):
    """Loads all modules that are in the same folder of `loader_file`.

    Args:
        loader_file (str): Full path of the file loading the modules
            that are in the same folder with it.

    Returns:
        dict: Dictionary mapping a module name to the corresponding
        module object.

    """
    modules = []
    root = pathlib.Path(loader_file).absolute().parent
    sys.path.insert(0, str(root.parent))

    # Find the subpackage where `root` is located, assuming `bci` is
    # the root package
    parents = [p.name for p in root.parents]
    subpackage = '.'.join(parents[parents.index('bci')::-1])

    # Import all modules in `root`
    for path in root.iterdir():
        if path.suffix == '.py' and not path.name.startswith('_'):
            modules.append(importlib.import_module(
                f'.{root.name}.{path.stem}',
                package=subpackage))

    return modules
