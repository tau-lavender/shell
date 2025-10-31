import os
import sys
import stat
from datetime import datetime
from pathlib import Path

import typer  # type: ignore

from src.log import logger
from src.enums.ls_output_mode import LsOutputMode


def ls(
    filename: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Dir to print",
    ),
    output_mode: bool = typer.Option(False, "-l", help="Add more information"),
    ) -> None:

    """
    List all files in a directory.
    :param filename:  path to directory to list
    :param output_mode:  optional Long list mode
    :return:  nothing
    """
    try:
        path = Path(filename)
        if not path.exists():
            logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(path)
        if not path.is_dir():
            logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(path)
        logger.info(f"Listing {path}")
        scan = sorted(list(os.scandir(path)), key=lambda x: x.name.lower())
        content = []
        single_str_output = ""
        enum_output_mode = LsOutputMode.LONG if output_mode else LsOutputMode.NORMAL
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
    except FileNotFoundError as e:
        print(f"File '{e}' not found")
    except NotADirectoryError as e:
        print(f"'{e}' not a directory")
    except OSError:
        print("[Error] OSError")
