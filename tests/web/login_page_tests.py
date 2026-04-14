import pytest
from faker import Faker

from src.web.application import Application
from tests.conftest import Config

faker = Faker()

invalid_login_params = [
    pytest.param(faker.email(), faker.password(length=50), id="fake_email_and_password"),
    pytest.param(faker.email(), faker.user_name(), id="fake_email_and_username_as_password"),
    pytest.param(faker.user_name(), faker.password(length=50), id="fake_username_as_email_and_password"),
    pytest.param("", faker.password(), id="empty_email"),
    pytest.param("invalidemail", faker.password(), id="no_at_symbol"),
    pytest.param(f"{faker.user_name()}@", faker.password(), id="no_domain"),
    pytest.param(f"{faker.user_name()}@domain", faker.password(), id="no_tld"),
    pytest.param(f"{faker.user_name()} @domain.com", faker.password(), id="space_in_email"),
    pytest.param(faker.email(), "", id="empty_password"),
    pytest.param(faker.email(), faker.lexify(text="?????"), id="too_short_password"),
    pytest.param(faker.email(), faker.password(length=7), id="password_7_below_min"),
    pytest.param(faker.email(), faker.password(length=8), id="password_8_min"),
    pytest.param(faker.email(), faker.password(length=9), id="password_9_above_min"),
    pytest.param(faker.email(), faker.password(length=72), id="password_72_max"),
    pytest.param(faker.email(), faker.password(length=73), id="password_73_above_max"),
    pytest.param("a", faker.password(), id="email_1_char"),
    pytest.param(f"{faker.lexify('a')}@b.c", faker.password(), id="shortest_valid_email"),
    pytest.param(f"{'a' * 243}@b.com", faker.password(), id="email_253"),
    pytest.param(f"{'a' * 244}@b.com", faker.password(), id="email_254"),
    pytest.param(f"{'a' * 245}@b.com", faker.password(), id="email_255"),
    pytest.param("admin' OR '1'='1", faker.password(), id="sql_injection_email"),
    pytest.param(faker.email(), "' OR '1'='1", id="sql_injection_password"),
    pytest.param("<script>alert(1)</script>", faker.password(), id="xss_email"),
    pytest.param(faker.email(), "<script>alert(1)</script>", id="xss_password"),
]


@pytest.mark.parametrize("email,password", invalid_login_params)
def test_login_invalid(shared_app: Application, email: str, password: str):
    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(email, password)
    shared_app.login_page.invalid_login_message_visible()

    shared_app.page.wait_for_timeout(2000)


def test_login_with_valid_creds(shared_app: Application, config: Config):
    shared_app.home_page.open()
    shared_app.home_page.is_loaded()
    shared_app.home_page.click_login()

    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(config.email, config.password)

    shared_app.projects_page.is_loaded()
