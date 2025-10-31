import sys
from pathlib import Path

import typer  # type: ignore

from src.log import logger
from src.enums.file_read_mode import FileReadMode


def cat(
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to print"
    ),
    raw_mode: bool = typer.Option(False, "--bytes", "-b", help="Read as bytes"),
    ) -> None:
    """
    Cat a file
    :param ctx: typer context object for imitating di container
    :param filename: Filename to cat
    :param raw_mode: Mode to read the file in
    :return:
    """
    try:
        mode = FileReadMode.BYTES if raw_mode else FileReadMode.STRING
        path = Path(filename)
        if not path.exists():
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(filename)
        if path.is_dir():
            logger.error(f"You entered {filename} is not a file")
            raise IsADirectoryError(filename)
        try:
            logger.info(f"Reading file {filename} in mode {mode}")
            match mode:
                case FileReadMode.STRING:
                    sys.stdout.write(path.read_text(encoding="utf-8"))
                case FileReadMode.BYTES:
                    sys.stdout.buffer.write(path.read_bytes())
        except OSError as e:
            logger.exception(f"Error reading {filename}: {e}")
    except FileNotFoundError as path:
        print(f"File not found: {path}")
    except IsADirectoryError as path:
        print(f"{path} - is not a file")
    except OSError as e:
        typer.echo(e)
