import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    # base_app_url: str
    email: str
    password: str
    login_url: str

@pytest.fixture(scope="session")
def config():
    return Config(
        login_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL"),
    )
