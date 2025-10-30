import importlib
import inspect
from src.configs.plagins_config import PLAGINS_IMPORT_CONFIG

from typer import Typer # type: ignore

from src.log import logger


app = Typer()


@app.callback()
def main():
    pass



if __name__ == "__main__":
    for plagin_name in PLAGINS_IMPORT_CONFIG:
        try:
            mod = importlib.import_module(plagin_name)
            functions = inspect.getmembers(mod, inspect.isfunction)
            app.command()(functions[0][1])
        except ImportError:
            logger.error(f"{plagin_name} not imported")
            print(f"{plagin_name} not imported")
    app()
