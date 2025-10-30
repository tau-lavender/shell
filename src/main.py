import importlib
import inspect
from src.configs.plagins_config import PLAGINS_IMPORT_CONFIG



# from src.configs.logger_config import LOGGING_CONFIG

# import logging
# import sys
# from pathlib import Path

import typer # type: ignore
from typer import Typer, Context


typer.echo("")
app = Typer()


@app.callback()
def main(ctx: Context):
    pass
    # logging.config.dictConfig(LOGGING_CONFIG)
    # logger = logging.getLogger(__name__)





# @app.command()
# def cat(
#     ctx: Context,
#     filename: Path = typer.Argument(
#         ..., exists=False, readable=False, help="File to print"
#     ),
#     mode: bool = typer.Option(False, "--bytes", "-b", help="Read as bytes"),
# ):
#     """
#     Cat a file
#     :param ctx: typer context object for imitating di container
#     :param filename: Filename to cat
#     :param mode: Mode to read the file in
#     :return:
#     """
#     try:
#         container: Container = get_container(ctx)
#         mode = FileReadMode.bytes if mode else FileReadMode.string
#         data = container.console_service.cat(
#             filename,
#             mode=mode,
#         )
#         if isinstance(data, bytes):
#             sys.stdout.buffer.write(data)
#         else:
#             sys.stdout.write(data)
#     except OSError as e:
#         typer.echo(e)


if __name__ == "__main__":
    for plagin_name in PLAGINS_IMPORT_CONFIG:
        try:
            mod = importlib.import_module(plagin_name)
            functions = inspect.getmembers(mod, inspect.isfunction)
            print(functions[0][1])
            app.add_typer(mod.app, name=plagin_name[plagin_name.rfind(".") + 1:])
        except ImportError:
            print(f"{plagin_name} not imported")
    app()
