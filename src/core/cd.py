import os
from pathlib import Path
from src.constants import PATH_TO_CURRENT_PATH

import typer  # type: ignore

from src.log import logger


def cd(
    filename: Path = typer.Argument(
        default=".", exists=False, readable=False, help="Dir to go",
    ),
    ) -> None:

    """
    Change working directory.
    :param filename:  path to directory to go
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
        logger.info(f"Change directory to {path}")
        with open(PATH_TO_CURRENT_PATH, "w") as f:
            current_path = os.getcwd()
            new_path = str(os.path.abspath(Path(current_path) / path))
            # print(new_path)
            f.write(new_path)
    except FileNotFoundError as path:
        print(f"Folder not found: {path}")
    except NotADirectoryError as path:
        print(f"You entered {path} is not a directory")
    except OSError:
        print("[Error] OSError")
