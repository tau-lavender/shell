import os
import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.errors import PathAlreadyExistsError


def mv(
    filename_from: Path = typer.Argument(
        ..., exists=False, readable=False, help="Откуда перемещать"
    ),
    filename_to: Path = typer.Argument(
        ..., exists=False, readable=False, help="Куда перемещать"
    ),
    ) -> None:
    """
    Премещает файл
    :param filename: Откуда перемещать
    :param raw_mode: Куда перемещать
    :return: Ничего
    """
    path_from = Path(filename_from)
    path_to = Path(filename_to)
    logger.info(f"mv {path_from} {path_to}")
    try:
        if not path_from.exists():
            raise FileNotFoundError(path_from)
        if path_from.is_file():
            if path_from.is_dir():
                raise IsADirectoryError(path_from)
            if path_to.exists():
                raise PathAlreadyExistsError(path_to)
            shutil.copy(path_from, path_to)
            os.remove(path=path_from)
        else:
            if path_from.is_file():
                raise NotADirectoryError(path_from)
            if path_to.is_dir():
                raise IsADirectoryError(path_to)
            if path_to.exists():
                raise PathAlreadyExistsError(path_to)
            shutil.copytree(path_from, path_to)
            os.rmdir(path=path_from)
        logger.info("Success")

    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except PathAlreadyExistsError as e_path:
        report_error(f"Path already exists: {e_path}")
    except IsADirectoryError as e_path:
        report_error(f"{e_path} - is not a file. If you want copy dir use '-r'")
    except NotADirectoryError as e_path:
        report_error(f"{e_path} - is not a dir")
    except PermissionError as e_path:
        report_error(f"Permission denied for file: {e_path}")
    except IOError as e:
        report_error(f"I/O error occurred: {e}")
    except OSError as e:
        report_error(f"OSError: {e}")
