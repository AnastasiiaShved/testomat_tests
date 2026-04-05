import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


@pytest.mark.regression
def test_login_with_valid_creds(app: Application, config: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(config.email, config.password)

    app.projects_page.is_loaded()


@pytest.mark.regression
def test_login_invalid_credentials(app: Application, config: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(config.email, Faker().password(length=50))
    app.login_page.invalid_login_message_visible()


@pytest.mark.regression
def test_projects_page_is_loaded(app: Application, login):
    app.projects_page.should_be_loaded()


@pytest.mark.regression
def test_projects_list_is_not_empty(app: Application, login):
    count = app.projects_page.get_projects_count()

    assert count > 0


@pytest.mark.regression
def test_project_search_returns_result(app: Application, login):
    app.page.pause()
    app.projects_page.search_project("P7roj12")
    app.projects_page.should_have_project("P7roj1")


@pytest.mark.regression
def test_new_project_creation(app: Application, login):
    target_project_name = Faker().company()

    (app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .submit_project_create())

    (app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (app.project_page
     .side_bar
     .is_loaded()
     .is_active('Tests'))
