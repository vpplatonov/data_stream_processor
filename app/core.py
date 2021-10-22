import importlib
from typing import List, Optional, Any


class DataStreamProcessor:

    def __init__(self, plugins: Optional[List] = None, path: str = "."):
        # Checking if plugin were sent
        if plugins:
            # create a list of plugins
            self._plugins = [
                # Import the module and initialise it at the same time
                importlib.import_module(plugin, path).Alerter() for plugin in plugins
            ]

    def run(self, df: Any = None, **kwargs):
        accumulator = {}
        # We is were magic happens, and all the plugins are going to be printed
        for plugin in self._plugins:
            key = str(plugin).split(".")[1]
            accumulator[key] = plugin.process(df, **kwargs)

        return accumulator
