import os
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.enums.rm_mode import RemoveMode
from src.errors import RootRemoveError, ParentRemoveError


def rm(
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="Что удалять"
    ),
    raw_mode: bool = typer.Option(False, "-r", help="Удаление папок внутри папок рекурсивно"),
    ) -> None:

    """
    Удаляет файл или папку
    :param filename: Что удалять
    :param raw_mode: Удаление папок внутри папок рекурсивно
    :return: Ничего
    """

    mode = RemoveMode.DIR if raw_mode else RemoveMode.FILE
    path = Path(filename)
    log_mode_fix = ""
    if raw_mode:
        log_mode_fix = " -r"
    logger.info(f"rm{log_mode_fix} {filename}")
    try:
        if filename == "..":
            raise ParentRemoveError()
        if str(filename) in "/\\":
            raise RootRemoveError()
        if not path.exists():
            raise FileNotFoundError(filename)
        match mode:
            case RemoveMode.FILE:
                if path.is_dir():
                    raise IsADirectoryError(filename)
                os.remove(path=path)
            case RemoveMode.DIR:
                if not path.is_dir():
                    raise NotADirectoryError(filename)
                print(f"remove {path} and all files inside y/n: ", end = "")
                if input() in ("y", "Y"):
                    os.rmdir(path=path)
        logger.info("Success")

    except RootRemoveError:
        report_error("Trying to remove root")
    except ParentRemoveError:
        report_error("Trying to remove parent folder")
    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except IsADirectoryError as e_path:
        report_error(f"{e_path} - is not a file. If you want remove dir use '-r'")
    except NotADirectoryError as e_path:
        report_error(f"{e_path} - is not a dir")
    except OSError as e:
        report_error(f"OSError: {e}")
