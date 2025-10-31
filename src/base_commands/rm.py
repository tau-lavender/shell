import os
from pathlib import Path

import typer  # type: ignore

from src.log import logger
from src.enums.rm_mode import RemoveMode


def rm(
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to remove"
    ),
    raw_mode: bool = typer.Option(False, "-r", help="Remove folder recursive"),
    ) -> None:
    """
    Remove a file
    :param filename: filename to remove
    :param raw_mode: Mode to remove dir recursive with all inside
    :return:
    """
    try:
        mode = RemoveMode.DIR if raw_mode else RemoveMode.FILE
        path = Path(filename)
        if not path.exists():
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(filename)
        try:
            match mode:
                case RemoveMode.FILE:
                    if path.is_dir():
                        logger.error(f"You entered {filename} is not a file")
                        raise IsADirectoryError(filename)
                    logger.info(f"Removing {filename}")
                    os.remove(path=path)
                case RemoveMode.DIR:
                    if not path.is_dir():
                        logger.error(f"You entered {filename} is not a dir")
                        raise NotADirectoryError(filename)
                    print(f"remove {path} and all files inside y/n: ", end = "")
                    if input() in ("y", "Y"):
                        logger.info(f"Removing dir {filename}")
                        os.rmdir(path=path)
        except OSError as e:
            logger.exception(f"Error reading {filename}: {e}")
    except FileNotFoundError as path:
        print(f"File not found: {path}")
    except IsADirectoryError as path:
        print(f"{path} - is not a file. If you want remove dir use '-r'")
    except NotADirectoryError as path:
        print(f"{path} - is not a dir")
    except OSError as e:
        typer.echo(e)
