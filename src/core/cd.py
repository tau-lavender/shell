import os
from pathlib import Path
from src.constants import PATH_TO_CURRENT_PATH

import typer  # type: ignore

from src.log import logger, report_error


def cd(
    filename: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Путь к директории",
    ),
    ) -> None:
    """
    Меняет рабочую директорию
    :filename: Путь к директории
    :return: Ничего
    """
    path = Path(filename)

    logger.info(f"cd {filename}")

    try:
        if not path.exists():
            raise FileNotFoundError(path)
        if not path.is_dir():
            raise NotADirectoryError(path)
        with open(PATH_TO_CURRENT_PATH, "w") as f:
            current_path = os.getcwd()
            new_path = str(os.path.abspath(Path(current_path) / path))
            f.write(new_path)
        logger.info("Success")

    except FileNotFoundError as e_path:
        report_error(f"Folder not found: {e_path}")
    except NotADirectoryError as e_path:
        report_error(f"{e_path} is not a directory")
    except OSError:
        report_error("[Error] OSError")
