import shutil
from pathlib import Path

import typer  # type: ignore

from src.log import logger


def untar(
    filename_archive: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Archive to unzip",
    ),
    ) -> None:

    """
    Untar
    :return:  nothing
    """
    try:
        path_archive = Path(filename_archive)
        if not path_archive.exists():
            logger.error(f"File not found: {path_archive}")
            raise FileNotFoundError(path_archive)
        if not str(path_archive).endswith(".tar.gz"):
            logger.error(f"{path_archive} is not a tar.")
            raise NotADirectoryError(path_archive)
        logger.info(f"Untar {path_archive}")
        shutil.unpack_archive(path_archive, str(path_archive)[:str(path_archive).rfind(".")], "gztar")
    except FileNotFoundError as e:
        print(f"File '{e}' not found")
    except NotADirectoryError as e:
        print(f"'{e}' not a directory")
    except OSError as e:
        print(f"[Error] OSError: {e}")
