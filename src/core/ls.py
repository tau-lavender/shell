import os
import sys
import stat
from datetime import datetime
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.enums.ls_output_mode import LsOutputMode


def ls_run(filename: Path, raw_mode: bool) -> None:
    """
    run ls
    :filename: путь к директории
    :output_mode: Режим расширенного вывода
    :return: Ничего
    """
    path = Path(filename)
    enum_output_mode = LsOutputMode.LONG if raw_mode else LsOutputMode.NORMAL
    log_mode_fix = ""
    if raw_mode:
        log_mode_fix = " -l"
    logger.info(f"ls{log_mode_fix} {filename}")
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_dir():
        raise NotADirectoryError(path)
    scan = sorted(list(os.scandir(path)), key=lambda x: x.name.lower())
    if len(scan) == 0:
        return None
    content = []
    single_str_output = ""
    match enum_output_mode:
        case LsOutputMode.NORMAL:
            for el in scan:
                if el.name[0] != ".":
                    single_str_output += el.name + " " * 2
            content.append(single_str_output)
        case LsOutputMode.LONG:
            size_max_wight = max(map(lambda x: len(str(x.stat().st_size)), scan))
            for el in scan:
                if el.name[0] != ".":
                    stats = el.stat()
                    mode = stats.st_mode
                    single_str_output = stat.filemode(mode) + " "
                    single_str_output += str(stats.st_size).rjust(size_max_wight) + " "
                    single_str_output += datetime.fromtimestamp(stats.st_mtime).strftime("%b %d %H:%M") + " "
                    single_str_output += el.name + "\n"
                    content.append(single_str_output)
    sys.stdout.writelines(content)
    logger.info("Success")


def ls(
    filename: Path = typer.Argument(
        default=".", exists=False, readable=False, help="путь к директории",
    ),
    raw_mode: bool = typer.Option(False, "-l", help="Режим расширенного вывода"),
    ) -> None:

    """
    Выводит все файлы в директории
    :filename: путь к директории
    :output_mode: Режим расширенного вывода
    :return: Ничего
    """

    try:
        ls_run(filename=filename, raw_mode=raw_mode)
    except FileNotFoundError as e_path:
        report_error(f"Folder not found: {e_path}")
    except NotADirectoryError as e_path:
        report_error(f"'{e_path}' not a directory")
    except OSError:
        report_error("[Error] OSError")
