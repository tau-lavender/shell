import os
import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.errors import FileWrongTypeError


def unzip(
    filename_archive: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Файл архива",
    ),
    ) -> None:

    """
    Извлекает из архива формата .zip одноимённую папку
    :filename_archive: Файл архива
    :return: Ничего
    """

    path_archive = Path(filename_archive)

    logger.info(f"unzip {path_archive}")
    try:
        if not path_archive.exists():
            raise FileNotFoundError(path_archive)
        if not str(path_archive).endswith(".zip"):
            raise FileWrongTypeError(path_archive)
        if not Path(path_archive.name[:path_archive.name.rfind(".zip")]).exists():
            os.mkdir(path_archive.name[:path_archive.name.rfind(".zip")])
        shutil.unpack_archive(path_archive, str(path_archive)[:str(path_archive).rfind(".zip")], "zip")
        logger.info("Success")

    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except FileWrongTypeError as e_path:
        report_error(f"{e_path} is not a zip.")
    except OSError as e:
        print(f"OSError: {e}")
