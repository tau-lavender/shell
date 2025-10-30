# import os
# import stat
# from datetime import datetime

import sys
from pathlib import Path

import typer # type: ignore
from typer import Typer, Context


app = Typer()


@app.command()
def cd(
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
