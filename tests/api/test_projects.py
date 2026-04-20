from src.api.projects_client import Project, ProjectsClient
from tests.fixtures.config import Config


def test_get_projects_returns_200(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert projects.status_code == 200


def test_get_projects_response_is_json(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert "application/vnd.api+json" in projects.headers["Content-Type"]


def test_get_projects_response_is_iterable(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    print(f"URL: {projects.url}")
    print(f"Total projects: {len(projects)}")
    for project in projects:
        print(f"Title: {project.title} - {project.status}")
        print(f"Id: {project.id}")
        print(f"Tests count: {project.tests_count}")
        print(f"URL: {project.url}")


def test_get_projects_list_is_not_empty(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    assert len(projects) > 0


def test_get_projects_items_have_required_fields(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert isinstance(project, Project)
        assert project.id
        assert project.type
        assert project.attributes


def test_get_projects_items_type_is_project(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert project.type == "project"


def test_get_projects_items_have_title(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        assert isinstance(project.title, str)
        assert len(project.title) > 0


def test_get_projects_items_have_slug(projects_client: ProjectsClient):
    projects = projects_client.get_projects()

    for project in projects:
        if project.slug is not None:
            assert isinstance(project.slug, str)
            assert len(project.slug) > 0


def test_get_projects_unauthorized(config: Config):
    projects = ProjectsClient.unauthorized(config.app_base_url).get_projects()

    assert projects.status_code == 403
