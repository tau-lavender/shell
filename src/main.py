import importlib
import inspect
from src.configs.plagins_config import PLAGINS_IMPORT_CONFIG

from typer import Typer, Context # type: ignore

from src.log import logger


app = Typer()


@app.callback()
def main(ctx: Context):
    pass


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
            app.command()(functions[0][1])
        except ImportError:
            logger.error(f"{plagin_name} not imported")
            print(f"{plagin_name} not imported")
    app()
