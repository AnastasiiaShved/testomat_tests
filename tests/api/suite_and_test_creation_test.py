import pytest
from faker import Faker

from src.api.controller import SuiteController, TestController, ProjectController
from src.api.models import Project
from tests.fixtures.api import project_controller

fake = Faker()


@pytest.mark.api
@pytest.mark.smoke
def test_suite_controller(
        project: Project,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    suite_name = fake.sentence()
    suite_response = suite_controller.create(project_id=project.id, title=suite_name, description=fake.paragraph())

    actual_test_suite = suite_controller.get_by_id(project.id, suite_response.id)

    assert suite_response.id == actual_test_suite.id
    assert suite_response.attributes.title == actual_test_suite.attributes.title
    assert actual_test_suite.attributes.title == suite_name


def test_create_suite_and_case(
        project_controller: ProjectController,
        suite_controller: SuiteController,
        test_controller: TestController,
):
    project = project_controller.get_all()[0]
    suite_name = fake.sentence()
    suite = suite_controller.create(project_id=project.id, title=suite_name)

    assert suite.id is not None
    assert suite.attributes.title == suite_name

    test_ui_title = fake.sentence()
    test_ui = test_controller.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_ui_title,
    )

    assert test_ui.id is not None
    assert test_ui.title == test_ui_title
    assert test_ui.suite_id == suite.id
