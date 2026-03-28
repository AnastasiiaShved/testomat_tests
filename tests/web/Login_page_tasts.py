from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


def test_login_invalid(app: Application, config: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(config.email, Faker().password(length=50))
    app.login_page.invalid_login_message_visible()


def test_login_with_valid_creds(app: Application, config: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(config.email, config.password)

    app.projects_page.is_loaded()
