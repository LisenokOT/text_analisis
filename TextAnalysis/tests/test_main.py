import pytest
from TextAnalysis.__main__ import DEFAULT_ARG
from TextAnalysis.main import main


@pytest.fixture
def userdata():
    """ Входные параметры пользователя """
    return DEFAULT_ARG

def test_runDefault(userdata):
    main(userdata)
