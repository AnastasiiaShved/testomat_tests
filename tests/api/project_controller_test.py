import pytest

from src.api.controller import ProjectController
from src.api.models import Project


@pytest.mark.api
def test_get_project_by_id(
        project: Project,
        project_controller: ProjectController,
):
    fetched = project_controller.get_by_id(project.id)

    assert fetched.id == project.id
    assert fetched.type == "project"


@pytest.mark.api
def test_project_has_title(
        project: Project,
        project_controller: ProjectController,
):
    fetched = project_controller.get_by_id(project.id)

    assert isinstance(fetched.title, str)
    assert len(fetched.title) > 0


@pytest.mark.api
def test_project_has_status(
        project: Project,
        project_controller: ProjectController,
):
    fetched = project_controller.get_by_id(project.id)

    assert isinstance(fetched.status, str)


@pytest.mark.api
def test_project_has_tests_count(
        project: Project,
        project_controller: ProjectController,
):
    fetched = project_controller.get_by_id(project.id)

    assert isinstance(fetched.tests_count, int)
    assert fetched.tests_count >= 0
