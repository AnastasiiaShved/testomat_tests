import os

import pytest
from playwright.sync_api import Browser

IS_CI = bool(os.getenv("CI"))

BROWSER_LAUNCH_ARGS = {
    "headless": IS_CI,
    "slow_mo": 0 if IS_CI else 700,
    "timeout": 30000,
}


@pytest.fixture(scope="session")
def browser_instance(playwright) -> Browser:
    browser = playwright.chromium.launch(**BROWSER_LAUNCH_ARGS)
    yield browser
    browser.close()
