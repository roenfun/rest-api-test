import pytest

from weixin.contact.weixin_token import Weixin


@pytest.fixture(scope="session")
def user_token():
    return Weixin.get_token_new()
