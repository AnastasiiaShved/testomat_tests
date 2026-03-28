from playwright.sync_api import expect

from src.web.Application import Application


def test_search_project(app: Application, login):
    app.projects_page.search_project("Proj1")
    app.projects_page.should_have_project("Proj1")


def test_projects_page_should_be_loaded(app: Application, login):
    app.projects_page.should_be_loaded()


def test_get_projects_count(app: Application, login):
    count = app.projects_page.get_projects_count()

    assert count > 0
    assert count == app.projects_page.project_cards.count()


def test_get_projects_count_dynamic(app: Application, login):
    app.projects_page.should_be_loaded()

    count_from_method = app.projects_page.get_projects_count()

    expect(app.projects_page.project_cards).to_have_count(count_from_method)

    print(count_from_method)


def test_project_page_header_flow(app: Application, login):
    target_project = "QA_SH"

    app.projects_page.should_be_loaded()
    app.projects_page.header.select_company("QA Club Lviv")
    expect(
        app.projects_page.header.company_select.locator("option:checked")
    ).to_have_text("QA Club Lviv")
    app.projects_page.header.search(target_project)

    project = app.projects_page.get_project_by_name(target_project)
    project.should_have_title(target_project)

    print(project.badges_count())


def test_print_project_badges(app: Application, login):
    target_project = "QA_SH"

    app.projects_page.should_be_loaded()
    app.projects_page.header.search(target_project)

    project = app.projects_page.get_project_by_name(target_project)
    project.should_have_title(target_project)
    badges = project.get_badges()

    print(badges)
