import importlib
import re
from typing import List, Optional, Any


def up_low_case(string, case):
    """Convert string into upper or lower case.

    Parameters
    ----------
    string: String to convert.

    Returns
    -------
    string: Uppercase or lowercase case string.
    """

    if case == 'up':
        return str(string).upper()
    elif case == 'low':
        return str(string).lower()


def camel_case(string):
    """
    Convert string into camel case.

    Parameters
    ----------
    string: String to convert.

    Returns
    -------
    string: Camel case string.
    """

    string = re.sub(r"^[\-_\.]", '', str(string))
    if not string:
        return string

    return (up_low_case(string[0], 'low') + re.sub(
        r"[\-_\.\s]([a-z])",
        lambda matched: up_low_case(matched.group(1), 'up'),
        string[1:]
    ))


def capital_case(string):
    """
    Convert string into capital case. First letters will be uppercase.

    Parameters
    ----------
    string: String to convert.

    Returns
    -------
    string: Capital case string.
    """

    string = str(string)
    if not string:
        return string

    return up_low_case(string[0], 'up') + string[1:]


def pascal_case(string):
    """
    Convert string into pascal case.

    Parameters
    ----------
    string: String to convert.

    Returns
    -------
    Pascal case string.
    """

    return capital_case(camel_case(string))


class PluginTestCaseError(Exception):
    """ raise exception if test case method not present in plugin """


class DataStreamProcessor:

    def __init__(self, plugins: Optional[List] = None, path: str = ".", logger=None):
        # Checking if plugin were sent
        if plugins:
            # create a list of plugins
            self._plugins = []
            # Import the module and initialise it at the same time
            for plugin in plugins:
                module = importlib.import_module(plugin, path)
                class_ = getattr(module, pascal_case(plugin.split('.').pop()))
                if hasattr(class_, 'test_case') and callable(getattr(class_, 'test_case')):
                    self._plugins.append(class_())
                elif logger is not None:
                    logger.error(f"Plugin {class_} SHELL have test_case() method")

    def run(self, df: Any = None, **kwargs):
        accumulator = {}
        # We is were magic happens, and all the plugins are going to be printed
        for plugin in self._plugins:
            key = str(plugin).split(".")[1]
            accumulator[key] = plugin.process(df, **kwargs)

        return accumulator
