import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger
from src.enums.cp_mode import CopyMode


class PathAlreadyExistsError(Exception):
    pass


def cp(
    filename_from: Path = typer.Argument(
        ..., exists=False, readable=False, help="What to copy"
    ),
    filename_were: Path = typer.Argument(
        ..., exists=False, readable=False, help="Where to copy"
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
        mode = CopyMode.DIR if raw_mode else CopyMode.FILE
        path_from = Path(filename_from)
        path_where = Path(filename_were)
        if not path_from.exists():
            raise FileNotFoundError(path_from)
        match mode:
            case CopyMode.FILE:
                if path_from.is_dir():
                    raise IsADirectoryError(path_from)
                if path_where.exists():
                    raise PathAlreadyExistsError(path_where)
                logger.info(f"Copy {path_from} to {path_where}")
                shutil.copy(path_from, path_where)
            case CopyMode.DIR:
                if not path_from.is_dir():
                    raise NotADirectoryError(path_from)
                if path_where.is_dir():
                    raise IsADirectoryError(path_where)
                if path_where.exists():
                    raise PathAlreadyExistsError(path_where)
                logger.info(f"Copy {path_from} to {path_where}")
                shutil.copytree(path_from, path_where)


    except FileNotFoundError as path:
        logger.error(f"File not found: {path}")
        print(f"File not found: {path}")

    except PathAlreadyExistsError as path:
        logger.error(f"Path already exists: {path}")
        print(f"Path already exists: {path}")

    except IsADirectoryError as path:
        logger.error(f"{path} - is not a file")
        print(f"{path} - is not a file. If you want remove dir use '-r'")

    except NotADirectoryError as path:
        logger.error(f"You entered {path} is not a dir")
        print(f"{path} - is not a dir")

    except PermissionError as path:
        logger.error(f"Permission denied for file: {path}")
        print(f"Permission denied for file: {path}")

    except IOError as path:
        logger.error(f"I/O error occurred: {path}")
        print(f"I/O error occurred: {path}")

    except OSError:
        logger.exception(f"Error copy: {path_from} to {path_where}")
        print(f"Error copy: {path_from} to {path_where}")
