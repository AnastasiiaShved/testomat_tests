import pytest

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper

FEATURE_FLAG_COOKIE = "feature_flag"
FEATURE_FLAG_VALUE = "enabled"


@pytest.fixture
def cookies(logged_app: Application) -> CookieHelper:
    return CookieHelper(logged_app.page.context)


def test_add_feature_flag_cookie(logged_app: Application, cookies: CookieHelper, config: Config):
    cookies.add(
        name=FEATURE_FLAG_COOKIE,
        value=FEATURE_FLAG_VALUE,
        domain=config.app_base_url,
    )

    assert cookies.exists(FEATURE_FLAG_COOKIE)
    assert cookies.get_value(FEATURE_FLAG_COOKIE) == FEATURE_FLAG_VALUE

    logged_app.page.reload()
    logged_app.page.wait_for_load_state("networkidle")


def test_clear_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    cookies.add(
        name=FEATURE_FLAG_COOKIE,
        value=FEATURE_FLAG_VALUE,
        domain=logged_app.page.url,
    )
    assert cookies.exists(FEATURE_FLAG_COOKIE)

    cookies.clear(name=FEATURE_FLAG_COOKIE)

    assert not cookies.exists(FEATURE_FLAG_COOKIE)
