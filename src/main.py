import os
import importlib
import inspect

from src.constants import PATH_TO_CURRENT_PATH
from src.configs.plugins_config import PLUGINS_IMPORT_CONFIG

from typer import Typer # type: ignore

from src.log import logger


app = Typer()


if __name__ == "__main__":
    try:
        with open(PATH_TO_CURRENT_PATH) as f:
            current_path = f.readline().rstrip()
    except FileNotFoundError:
        with open(PATH_TO_CURRENT_PATH, "w") as f:
            current_path = os.getcwd()
            f.write(current_path)
    os.chdir(path=current_path)

    for plugin_name in PLUGINS_IMPORT_CONFIG:
        try:
            mod = importlib.import_module(plugin_name)
            functions = inspect.getmembers(mod, inspect.isfunction)
            app.command()(functions[0][1])
        except ImportError:
            logger.error(f"{plugin_name} not imported")
            print(f"{plugin_name} not imported")

    app()
