import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.Application import Application
from src.web.pages.LoginPage import LoginPage

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    # base_app_url: str
    email: str
    password: str
    login_url: str

@pytest.fixture(scope="session")
def config():
    return Config(
        login_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL"),
    )


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(page: Page, config: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(config.email, config.password)
