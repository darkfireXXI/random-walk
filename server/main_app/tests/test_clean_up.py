import pytest


@pytest.mark.usefixtures("clean_db", autouse=True)
def test_clean_up():
    pass
