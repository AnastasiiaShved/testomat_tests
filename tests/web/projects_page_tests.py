import pytest
from playwright.sync_api import expect

from src.web.Application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_search_project(logged_app: Application):
    logged_app.projects_page.search_project("Proj1")
    logged_app.projects_page.should_have_project("Proj1")


def test_projects_page_should_be_loaded(logged_app: Application):
    logged_app.projects_page.should_be_loaded()


@pytest.mark.smoke
@pytest.mark.web
def test_get_projects_count(logged_app: Application):
    count = logged_app.projects_page.get_projects_count()

    assert count > 0
    assert count == logged_app.projects_page.project_cards.count()


def test_get_projects_count_dynamic(logged_app: Application):
    logged_app.projects_page.should_be_loaded()

    count_from_method = logged_app.projects_page.get_projects_count()

    expect(logged_app.projects_page.project_cards).to_have_count(count_from_method)

    print(count_from_method)


def test_project_page_header_flow(logged_app: Application):
    target_project = "QA_SH"

    logged_app.projects_page.should_be_loaded()
    logged_app.projects_page.header.select_company("QA Club Lviv")
    expect(
        logged_app.projects_page.header.company_select.locator("option:checked")
    ).to_have_text("QA Club Lviv")
    logged_app.projects_page.header.search(target_project)

    project = logged_app.projects_page.get_project_by_name(target_project)
    project.should_have_title(target_project)

    print(project.badges_count())


@pytest.mark.smoke
@pytest.mark.web
def test_print_project_badges(logged_app: Application):
    target_project = "QA_SH"

    logged_app.projects_page.should_be_loaded()
    logged_app.projects_page.header.search(target_project)

    project = logged_app.projects_page.get_project_by_name(target_project)
    project.should_have_title(target_project)
    badges = project.get_badges()

    print(badges)
