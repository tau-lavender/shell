import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.errors import PathAlreadyExistsError


def zip(
    filename_dir: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Что архивировать",
    ),
    filename_archive: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Файл в который сохранится архив",
    ),
    ) -> None:

    """
    Создаёт из папки архив формата .zip
    :filename_dir: Что архивировать
    :filename_archive: Файл в который сохранится архив
    :return: Ничего
    """

    path_dir = Path(filename_dir)
    path_archive = Path(filename_archive)

    logger.info(f"tar {filename_dir} {filename_archive}")

    try:
        if not path_dir.exists():
            raise FileNotFoundError(path_dir)
        if path_archive.exists():
            raise PathAlreadyExistsError(path_archive)
        if not path_dir.is_dir():
            raise NotADirectoryError(path_dir)
        if str(path_archive).endswith(".zip"):
            path_archive = Path(str(path_archive)[:-4])
        shutil.make_archive(str(path_archive), "zip", path_dir)
        logger.info("Success")

    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except PathAlreadyExistsError as e_path:
        report_error(f"Path already exists: {e_path}")
    except NotADirectoryError as e_path:
        report_error(f"{e_path} is not a directory")
    except OSError as e:
        report_error(f"OSError: {e}")
