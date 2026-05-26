import pytest
import requests
from faker import Faker

from src.api.controller import SuiteController
from src.api.models import Project

fake = Faker()


@pytest.mark.api
def test_create_suite_with_description(
        project: Project,
        suite_controller: SuiteController,
):
    title = fake.sentence()
    description = fake.paragraph()

    suite = suite_controller.create(project_id=project.id, title=title, description=description)

    assert suite.id is not None
    assert suite.attributes.title == title
    assert suite.attributes.description == description

    fetched = suite_controller.get_by_id(project.id, suite.id)
    assert fetched.attributes.title == title
    assert fetched.attributes.description == description


@pytest.mark.api
def test_create_suite_without_description(
        project: Project,
        suite_controller: SuiteController,
):
    title = fake.sentence()

    suite = suite_controller.create(project_id=project.id, title=title)

    assert suite.id is not None
    assert suite.attributes.title == title
    assert suite.attributes.description is None


@pytest.mark.api
def test_get_suite_by_id(
        project: Project,
        suite_controller: SuiteController,
):
    title = fake.sentence()
    created = suite_controller.create(project_id=project.id, title=title)

    fetched = suite_controller.get_by_id(project.id, created.id)

    assert fetched.id == created.id
    assert fetched.attributes.title == title


@pytest.mark.api
def test_update_suite_title(
        project: Project,
        suite_controller: SuiteController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    new_title = fake.sentence()

    updated = suite_controller.update(project_id=project.id, suite_id=suite.id, title=new_title)

    assert updated.attributes.title == new_title

    fetched = suite_controller.get_by_id(project.id, suite.id)
    assert fetched.attributes.title == new_title


@pytest.mark.api
def test_delete_suite(
        project: Project,
        suite_controller: SuiteController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())

    suite_controller.delete(project_id=project.id, suite_id=suite.id)

    with pytest.raises(requests.HTTPError) as exc_info:
        suite_controller.get_by_id(project.id, suite.id)
    assert exc_info.value.response.status_code == 404


@pytest.mark.api
def test_create_suite_invalid_project(
        suite_controller: SuiteController,
):
    with pytest.raises(requests.HTTPError) as exc_info:
        suite_controller.create(project_id="nonexistent-project-id", title=fake.sentence())
    assert exc_info.value.response.status_code in (404, 422)
