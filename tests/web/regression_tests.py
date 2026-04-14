import pytest
from faker import Faker

from src.web.application import Application
from tests.conftest import Config, Projects


@pytest.mark.regression
def test_login_with_valid_creds(shared_app: Application, config: Config):
    shared_app.home_page.open()
    shared_app.home_page.is_loaded()
    shared_app.home_page.click_login()

    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(config.email, config.password)

    shared_app.projects_page.is_loaded()


@pytest.mark.regression
def test_login_invalid_credentials(shared_app: Application, config: Config):
    shared_app.home_page.open()
    shared_app.home_page.is_loaded()
    shared_app.home_page.click_login()

    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(config.email, Faker().password(length=50))
    shared_app.login_page.invalid_login_message_visible()


@pytest.mark.regression
def test_projects_page_is_loaded(logged_app: Application):
    logged_app.projects_page.should_be_loaded()


@pytest.mark.regression
def test_projects_list_is_not_empty(logged_app: Application):
    count = logged_app.projects_page.get_projects_count()

    assert count > 0


@pytest.mark.regression
def test_project_search_returns_result(logged_app: Application):
    logged_app.projects_page.search_project(Projects.SEARCH_PROJECT)
    logged_app.projects_page.should_have_project(Projects.SEARCH_PROJECT)


@pytest.mark.regression
def test_new_project_creation(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .submit_project_create())

    (logged_app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (logged_app.project_page
     .side_bar
     .is_loaded()
     .is_active('Tests'))
