import pytest

from src.api.projects_client import ProjectsClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def projects_client(config: Config) -> ProjectsClient:
    return ProjectsClient(config.app_base_url, config.api_token)
