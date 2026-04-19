import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import clear_browser_state

STORAGE_STATE_PATH = Path("test_result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH: Path = Path("test_result/.auth/free_storage_state.json")

BROWSER_CONTEXT_ARGS = {
    "base_url": os.getenv("BASE_APP_URL"),
    "viewport": {"width": 1320, "height": 980},
    "locale": "uk_UA",
    "timezone_id": "Europe/Kyiv",
    "record_video_dir": "videos/",
    "permissions": ["geolocation"],
}


def create_free_project_state() -> None:
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ''
            break
    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_context(
        browser: Browser,
        base_url: str,
        storage_state_path: Path | None = None,
) -> BrowserContext:
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1320, "height": 980},
        "locale": "uk_UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }
    if storage_state_path and storage_state_path.exists():
        kwargs["storage_state"] = str(storage_state_path)
    return browser.new_context(**kwargs)


@pytest.fixture(scope="session")
def shared_context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(**BROWSER_CONTEXT_ARGS)
    ctx.new_page()
    yield ctx
    ctx.close()


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, config: Config) -> BrowserContext:
    if STORAGE_STATE_PATH.exists():
        ctx = build_browser_context(browser_instance, config.app_base_url, storage_state_path=STORAGE_STATE_PATH)
        yield ctx
        ctx.close()
        return

    ctx = build_browser_context(browser_instance, config.app_base_url)
    page = ctx.new_page()
    app = Application(page, config.base_url, config.app_base_url)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(config.email, config.password)
    app.projects_page.should_be_loaded()
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ctx.storage_state(path=str(STORAGE_STATE_PATH))
    create_free_project_state()

    yield page
    ctx.close()


@pytest.fixture(scope="function")
def shared_app(shared_context: BrowserContext, config: Config) -> Application:
    page = shared_context.pages[0]
    clear_browser_state(page)
    yield Application(page, config.base_url, config.app_base_url)
    clear_browser_state(page)


@pytest.fixture(scope="function")
def logged_app(logged_page: BrowserContext, config: Config) -> Application:
    logged_page.goto("/projects/")
    yield Application(logged_page, config.base_url, config.app_base_url)
    logged_page.close()


@pytest.fixture(scope="session")
def free_project_context(browser_instance: Browser, config: Config) -> Page:
    if FREE_PROJECT_STORAGE_PATH.exists():
        context = build_browser_context(browser_instance, config.app_base_url,
                                        storage_state_path=FREE_PROJECT_STORAGE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser_instance, config.app_base_url)
    page = context.new_page()
    app = Application(page, config.base_url, config.app_base_url)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(config.email, config.password)
    app.projects_page.should_be_loaded()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()
    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(FREE_PROJECT_STORAGE_PATH))
    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_context: Page, config: Config) -> Application:
    free_project_context.goto("/projects/")
    yield Application(free_project_context, config.base_url, config.app_base_url)
