import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.errors import FileWrongTypeError


def untar(
    filename_archive: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Файл архива",
    ),
    ) -> None:

    """
    Извлекает из архива формата .tar.gz папку .tar
    :filename_archive: Файл архива
    :return: Ничего
    """

    path_archive = Path(filename_archive)

    logger.info(f"untar {path_archive}")
    try:
        if not path_archive.exists():
            raise FileNotFoundError(path_archive)
        if not str(path_archive).endswith(".tar.gz"):
            raise FileWrongTypeError(path_archive)
        shutil.unpack_archive(path_archive, str(path_archive)[:str(path_archive).rfind(".")], "gztar")
        logger.info("Success")

    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except FileWrongTypeError as e_path:
        report_error(f"{e_path} is not a tar.")
    except OSError as e:
        report_error(f"OSError: {e}")
