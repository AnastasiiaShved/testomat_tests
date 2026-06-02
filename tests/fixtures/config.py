import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv(override=True)


class Projects:
    SEARCH_PROJECT = "Proj1"
    TARGET_PROJECT = "QA_SH"
    EXPECTED_PLAN = "Enterprise Plan"


class Companies:
    QA_CLUB_LVIV = "QA Club Lviv"


@dataclass(frozen=True)
class Config:
    base_url: str
    email: str
    password: str
    app_base_url: str
    api_token: str


@pytest.fixture(scope="session")
def config() -> Config:
    return Config(
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL"),
        api_token=os.getenv("API_TOKEN"),
    )
