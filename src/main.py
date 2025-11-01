import os
import importlib
import inspect

from typer import Typer # type: ignore

from src.log import logger
from src.configs.plugins_config import PLUGINS_IMPORT_CONFIG
from src.constants import PATH_TO_CURRENT_PATH


app = Typer()


if __name__ == "__main__":
    # загружает файл где xранится cwd, создаёт если не существует
    try:
        with open(PATH_TO_CURRENT_PATH) as f:
            current_path = f.readline().rstrip()
    except FileNotFoundError:
        with open(PATH_TO_CURRENT_PATH, "w") as f:
            current_path = os.getcwd()
            f.write(current_path)
    os.chdir(path=current_path)

    # импортирует команды обьявленные в конфиге
    for plugin_name in PLUGINS_IMPORT_CONFIG:
        try:
            mod = importlib.import_module(plugin_name)
            functions = inspect.getmembers(mod, inspect.isfunction)
            for foo in functions:
                if foo[0] == plugin_name[plugin_name.rfind(".") + 1:]:
                    app.command()(foo[1])
                    break
            else:
                raise ImportError
        except ImportError:
            print(f"{plugin_name} not imported")
            logger.error(f"{plugin_name} not imported")

    # запускает приложение typer
    try:
        app()
    except OSError as e:
        print(f"OSError: {e}")
        logger.error(f"OSError: {e}")
