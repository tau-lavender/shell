import pytest

from tests.fixtures import create_temp_dir # type: ignore

from src.core.ls import ls_run
from src.core.cd import cd_run
from src.core.cat import cat_run


create_temp_dir()

@pytest.mark.usefixtures("create_temp_dir")
def test_ls():
    ls_run(".", False)
    ls_run(".temp_test/c", False)
    ls_run(".", True)
    ls_run(".temp_test/d", True)
    with pytest.raises(FileNotFoundError):
        ls_run(".temp_test/aboba", True)
    with pytest.raises(NotADirectoryError):
        ls_run(".temp_test/a.txt", True)


@pytest.mark.usefixtures("create_temp_dir")
def test_cd():
    cd_run(".temp_test/")
    cd_run("..")
    cd_run(".temp_test/d")
    cd_run("..")
    with pytest.raises(FileNotFoundError):
        cd_run(".temp_test/aboba")
    with pytest.raises(NotADirectoryError):
        cd_run(".temp_test/a.txt")


@pytest.mark.usefixtures("create_temp_dir")
def test_cat():
    cat_run(".temp_test/a.txt", False)
    cat_run(".temp_test/b.txt", True)
    with pytest.raises(FileNotFoundError):
        cat_run(".temp_test/aboba.txt", False)
    with pytest.raises(IsADirectoryError):
        cat_run(".temp_test/c", False)
