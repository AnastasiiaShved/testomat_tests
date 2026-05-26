import pytest
import requests

from src.api.controller.project_controller import ProjectController
from src.api.controller.suite_controller import SuiteController
from src.api.controller.test_controller import TestController
from src.api.models.project import Project
from src.api.projects_client import ProjectsClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def projects_client(config: Config) -> ProjectsClient:
    return ProjectsClient(config.app_base_url, config.api_token)


@pytest.fixture(scope="session")
def auth_token(config: Config) -> str:
    response = requests.post(
        url=f"{config.app_base_url}/api/login",
        json={"api_token": config.api_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_controller(config: Config, auth_token: str) -> ProjectController:
    controller = ProjectController(
        base_url=config.app_base_url,
        api_token=config.api_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def suite_controller(config: Config, auth_token: str) -> SuiteController:
    controller = SuiteController(
        base_url=config.app_base_url,
        api_token=config.api_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def test_controller(config: Config, auth_token: str) -> TestController:
    controller = TestController(
        base_url=config.app_base_url,
        api_token=config.api_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="function")
def project(project_controller: ProjectController) -> Project:
    projects = project_controller.get_all()
    return projects[0]
