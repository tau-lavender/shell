# import os
# import stat
# from datetime import datetime

import sys
from pathlib import Path

import typer # type: ignore
from typer import Typer, Context

app = Typer()

# def ls(self, path, arg = {}):
#     scan = os.scandir(path)
#     if "l" not in arg:
#         for el in scan:
#             if el.name[0] != ".":
#                 print(el.name, end = "  ")
#         print()
#     else:
#         scan = list(scan)
#         size_max_wight = max(map(lambda x: len(str(x.stat().st_size)), scan))
#         name_max_wight = max(map(lambda x: len(x.name) * (x.name[0] != "."), scan))
#         for el in scan:
#             if el.name[0] != ".":
#                 stats = el.stat()
#                 mode = stats.st_mode
#                 print(stat.filemode(mode), end = "   ")
#                 print(str(stats.st_size).rjust(size_max_wight), end = "   ")
#                 print(datetime.fromtimestamp(stats.st_mtime).strftime("%b %d %H:%M"), end = "   ")
#                 print(el.name.rjust(name_max_wight))

@app.command()
def ls(
    ctx: Context,
    path: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to print"
    ),
    ) -> None:

    """
    List all files in a directory.
    :param ctx:   typer context object for imitating di container
    :param path:  path to directory to list
    :return: content of directory
    """
    try:
        # container: Container = get_container(ctx)
        # content = container.console_service.ls(path)
        content = "LS used"
        sys.stdout.writelines(content)
    except OSError as e:
        typer.echo(e)

# path = os.getcwd()
# ls(path=path, arg=["l"])
