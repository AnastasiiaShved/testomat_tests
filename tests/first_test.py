import os

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.conftest import Config

TARGET_PROJECT = "QA_SH"

PROJECT_NAME = Faker().name()


@pytest.fixture(scope="function")
def login(page: Page, config: Config):
    page.goto(config.login_url)
    login_user(page, config.email, config.password)


def test_login_with_invalid_creds(page: Page, config: Config):
    open_home_page(page)
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()
    invalid_pasw = Faker().password(length=50)
    print(invalid_pasw)

    login_user(page, config.email, invalid_pasw)

    expect(page.locator('#content-desktop').get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator('#content-desktop .common-flash-info')).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_should_be_possible_to_select_free_project(page: Page, login):
    # act
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    # assert
    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()


def test_should_be_possible_to_open_free_project(page: Page, login):
    page.locator("#company_id").click()

    page.locator("#company_id").select_option("Free Projects")

    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def test_should_be_possible_to_open_new_project(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    page.get_by_role("link", name="Create Project").click()
    expect(page.get_by_role("heading", name="New Project")).to_be_visible()


def test_create_new_project_free(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    page.get_by_role("link", name="Create Project").click()
    page.get_by_role("textbox", name="Project Title").fill(PROJECT_NAME)
    page.locator("input[value='Create']").click()
    expect(page.get_by_role("heading", name='Welcome to Testomat.io')).to_be_visible()


def test_create_new_project_qa_club(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("QA Club Lviv")
    page.get_by_role("link", name="Create").click()
    page.get_by_role("textbox", name="Project Title").fill(PROJECT_NAME)
    page.locator("input[value='Create']").click()
    expect(page.get_by_role("heading", name='Welcome to Testomat.io')).to_be_visible()


def search_for_project(page: Page, TARGET_PROJECT: str):
    expect(page.get_by_role(role="searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(TARGET_PROJECT)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()


def open_home_page(page: Page):
    page.goto(os.getenv("BASE_URL"))
