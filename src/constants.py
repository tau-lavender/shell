import os
from pathlib import Path


PATH_TO_ROOT = Path(os.path.abspath(__file__)) / ".." / ".."

PATH_TO_CURRENT_PATH = os.path.abspath(PATH_TO_ROOT / ".current_path")
