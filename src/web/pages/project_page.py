from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import SideBar
from src.web.components.test_for_suite_popup import TestForSuitePopup
from src.web.components.test_modal import TestModal


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self.test_for_suite_popup = TestForSuitePopup(page)
        self.test_modal = TestModal(page)

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.locator("[placeholder = 'First Suite']")).to_be_visible()
        expect(self.page.get_by_role("button", name='Suite')).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def create_test_via_popup(self) -> Self:
        self.page.locator(".sticky-header").get_by_role("button", name="Test", exact=True).click()
        return self

    def create_suite_via_popup(self) -> Self:
        self.page.get_by_role("button", name="Suite ", exact=True).click()
        return self

    def has_first_suite_placeholder(self) -> bool:
        return self.page.locator("[placeholder='First Suite']").is_visible()

    def create_first_suite(self, suite_name: str) -> Self:
        self.page.locator("[placeholder='First Suite']").fill(suite_name)
        self.page.keyboard.press("Enter")
        return self

    def create_test_suite_via_popup(self):
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()

    def suite_with_name_is_visible(self, test_suite_name: str):
        expect(self.page.locator(".nested-item-row-suite").get_by_text(test_suite_name)).to_be_visible()
