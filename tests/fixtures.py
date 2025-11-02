import pytest
import os
import shutil


@pytest.fixture
def create_temp_dir():
    if os.path.exists(".temp_test"):
        shutil.rmtree(".temp_test")
    os.mkdir(".temp_test")
    os.mkdir(".temp_test/c")
    os.mkdir(".temp_test/d")
    with open(".temp_test/a.txt", "w") as f:
        f.write("aaaaa")
    with open(".temp_test/b.txt", "w") as f:
        f.write("b")
    with open(".temp_test/c/e.txt", "w") as f:
        f.write("b")
