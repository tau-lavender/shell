import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger

from src.errors import PathAlreadyExistsError


def zip(
    filename_dir: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Dir to zip",
    ),
    filename_archive: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Where zip go",
    ),
    ) -> None:

    """
    Zip
    :return:  nothing
    """
    try:
        path_dir = Path(filename_dir)
        path_archive = Path(filename_archive)
        if not path_dir.exists():
            logger.error(f"Folder not found: {path_dir}")
            raise FileNotFoundError(path_dir)
        if path_archive.exists():
            logger.error(f"Path already exists: {path_archive}")
            raise PathAlreadyExistsError(path_archive)
        if not path_dir.is_dir():
            logger.error(f"{path_dir} is not a directory")
            raise NotADirectoryError(path_dir)
        logger.info(f"Zip {path_dir} to {path_archive}")
        if str(path_archive).endswith(".zip"):
            path_archive = Path(str(path_archive)[:-4])
        shutil.make_archive(str(path_archive), "zip", path_dir)
    except FileNotFoundError as e:
        print(f"File '{e}' not found")
    except NotADirectoryError as e:
        print(f"'{e}' not a directory")
    except OSError as e:
        print(f"[Error] OSError: {e}")
