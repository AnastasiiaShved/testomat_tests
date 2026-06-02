import pytest
from faker import Faker

from src.api.projects_client import ProjectsClient
from src.web.application import Application


@pytest.mark.smoke
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


def test_new_project_creation_and_test_popup(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_project_page.open().is_loaded().fill_project_title(target_project_name).click_create())

    project_page = logged_app.project_page
    (project_page.is_loaded().empty_project_name_is(target_project_name).close_read_me())

    (project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests"))

    target_suite_name = Faker().company()
    project_page.create_first_suite(target_suite_name)
    project_page.create_test_via_popup()
    logged_app.test_for_suite_popup.is_loaded().select_first_suite()

    test_name = Faker().sentence()
    logged_app.test_modal.is_loaded("test").set_title(test_name).save()
    logged_app.test_modal.edit_is_visible("test")


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_from_side_bar(logged_app: Application, projects_client: ProjectsClient):
    all_projects = projects_client.get_projects()
    target_project_id = all_projects.data[1].id

    logged_app.project_page.open_by_id(target_project_id).side_bar.is_loaded()
    if logged_app.project_page.has_first_suite_placeholder():
        logged_app.project_page.create_first_suite(Faker().company())
    logged_app.project_page.create_test_via_popup()
    logged_app.test_for_suite_popup.is_loaded().select_first_suite()

    test_name = Faker().company()
    logged_app.test_modal.is_loaded().set_title(test_name).save()
    logged_app.test_modal.edit_is_visible()


def test_open_project_and_create_test_suite_from_side_bar(logged_app: Application, projects_client: ProjectsClient):
    all_projects = projects_client.get_projects()
    target_project_id = all_projects.data[1].id

    logged_app.project_page.open_by_id(target_project_id).side_bar.is_loaded()
    logged_app.project_page.create_test_suite_via_popup()

    test_name = Faker().company()
    logged_app.test_modal.is_loaded("Suite").set_title(test_name).save()
    logged_app.project_page.suite_with_name_is_visible(test_name)
