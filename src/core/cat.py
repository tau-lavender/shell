import sys
from pathlib import Path

import typer  # type: ignore

from src.log import logger, report_error
from src.enums.file_read_mode import FileReadMode


def cat_run(filename, raw_mode):
    """
    run cat
    :filename: Путь к файлу который надо вывести
    :raw_mode: Режим чтения файла
    :return: Ничего
    """

    mode = FileReadMode.BYTES if raw_mode else FileReadMode.STRING
    path = Path(filename)

    log_mode_fix = ""
    if raw_mode:
        log_mode_fix = " -b"
    logger.info(f"cat{log_mode_fix} {filename}")
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_dir():
        raise IsADirectoryError(path)
    match mode:
        case FileReadMode.STRING:
            sys.stdout.write(path.read_text(encoding="utf-8"))
        case FileReadMode.BYTES:
            sys.stdout.buffer.write(path.read_bytes())
    logger.info("Success")


def cat(
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="Путь к файлу"
    ),
    raw_mode: bool = typer.Option(False, "--bytes", "-b", help="Режим чтения байтами"),
    ) -> None:
    """
    Выводит файл в консоль
    :filename: Путь к файлу который надо вывести
    :raw_mode: Режим чтения файла
    :return: Ничего
    """

    try:
        cat_run(filename, raw_mode)
    except FileNotFoundError as e_path:
        report_error(f"File not found: {e_path}")
    except IsADirectoryError as e_path:
        report_error(f"{e_path} is not a file")
    except OSError as e:
        report_error(f"OSError {filename}: {e}")
