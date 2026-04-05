import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext

from src.web.Application import Application

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    email: str
    password: str
    app_base_url: str


@pytest.fixture(scope="session")
def config():
    return Config(
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL"),
    )


BROWSER_LAUNCH_ARGS = {
    "headless": False,
    "slow_mo": 700,
    "timeout": 30000,
}

BROWSER_CONTEXT_ARGS = {
    "base_url": os.getenv("BASE_APP_URL"),
    "viewport": {"width": 1320, "height": 980},
    "locale": "uk_UA",
    "timezone_id": "Europe/Kyiv",
    "record_video_dir": "videos/",
    "permissions": ["geolocation"],
}


@pytest.fixture(scope="session")
def browser_instance(playwright) -> Browser:
    browser = playwright.chromium.launch(**BROWSER_LAUNCH_ARGS)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def shared_context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(**BROWSER_CONTEXT_ARGS)
    ctx.new_page()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def shared_app(shared_context: BrowserContext) -> Application:
    clear_browser_state(shared_context)
    page = shared_context.pages[0]
    yield Application(page)
    clear_browser_state(shared_context)


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(**BROWSER_CONTEXT_ARGS)
    ctx.new_page()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext, config: Config) -> Application:
    page = logged_context.pages[0]
    application = Application(page)
    application.login_page.open()
    application.login_page.is_loaded()
    application.login_page.login_user(config.email, config.password)
    application.projects_page.should_be_loaded()
    yield application
    clear_browser_state(logged_context)


def clear_browser_state(context: BrowserContext) -> None:
    for page in context.pages:
        try:
            page.evaluate("localStorage.clear()")
            page.evaluate("sessionStorage.clear()")
        except Exception:
            pass
    for page in context.pages:
        page.goto("about:blank")
    context.clear_cookies()
