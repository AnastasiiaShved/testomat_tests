import pytest
import requests
from faker import Faker

from src.api.controller import SuiteController, TestController
from src.api.models import Project

fake = Faker()


@pytest.mark.api
def test_create_test_case(
        project: Project,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    title = fake.sentence()

    test = test_controller.create(project_id=project.id, suite_id=suite.id, title=title)

    assert test.id is not None
    assert test.title == title
    assert test.suite_id == suite.id


@pytest.mark.api
def test_get_test_by_id(
        project: Project,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    title = fake.sentence()
    created = test_controller.create(project_id=project.id, suite_id=suite.id, title=title)

    fetched = test_controller.get_by_id(project.id, created.id)

    assert fetched.id == created.id
    assert fetched.title == title


@pytest.mark.api
def test_update_test_title(
        project: Project,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    test = test_controller.create(project_id=project.id, suite_id=suite.id, title=fake.sentence())
    new_title = fake.sentence()

    updated = test_controller.update(project_id=project.id, test_id=test.id, title=new_title)

    assert updated.title == new_title


@pytest.mark.api
def test_delete_test(
        project: Project,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    test = test_controller.create(project_id=project.id, suite_id=suite.id, title=fake.sentence())

    test_controller.delete(project_id=project.id, test_id=test.id)

    with pytest.raises(requests.HTTPError) as exc_info:
        test_controller.get_by_id(project.id, test.id)
    assert exc_info.value.response.status_code == 404
