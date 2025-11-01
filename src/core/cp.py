import shutil

import typer  # type: ignore

from pathlib import Path

from src.log import logger, report_error
from src.enums.cp_mode import CopyMode
from src.errors import PathAlreadyExistsError


def cp(
    filename_from: Path = typer.Argument(
        ..., exists=False, readable=False, help="Откуда копировать"
    ),
    filename_to: Path = typer.Argument(
        ..., exists=False, readable=False, help="Куда копировать"
    ),
    raw_mode: bool = typer.Option(False, "-r", help="Копирование файлов внутри папки рекурсивно"),
    ) -> None:
    """
    Копирует файл
    :filename_from: Откуда копировать
    :filename_to: Куда копировать
    :raw_mode: Копирование файлов внутри папки рекурсивно
    :return:
    """

    mode = CopyMode.DIR if raw_mode else CopyMode.FILE
    path_from = Path(filename_from)
    path_to = Path(filename_to)

    log_mode_fix = ""
    if raw_mode:
        log_mode_fix = " -r"
    logger.info(f"cp{log_mode_fix} {filename_from} {filename_to}")

    try:
        if not path_from.exists():
            raise FileNotFoundError(path_from)
        match mode:
            case CopyMode.FILE:
                if path_from.is_dir():
                    raise IsADirectoryError(path_from)
                if path_to.exists():
                    raise PathAlreadyExistsError(path_to)
                shutil.copy(path_from, path_to)

            case CopyMode.DIR:
                if not path_from.is_dir():
                    raise NotADirectoryError(path_from)
                if path_to.is_dir():
                    raise IsADirectoryError(path_to)
                if path_to.exists():
                    raise PathAlreadyExistsError(path_to)
                shutil.copytree(path_from, path_to)
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
