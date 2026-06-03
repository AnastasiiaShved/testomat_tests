import allure
from playwright.sync_api import Page, expect

from src.web.components.project_card import ProjectCard
from src.web.components.project_page_header import ProjectsPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsPageHeader(page)
        self.grid = page.locator("#grid")
        self.project_cards = page.locator("#grid li")
        self.success_message = page.locator(".common-flash-success")
        self.info_message = page.locator(".common-flash-info")

    @allure.step
    def open(self):
        self.page.goto("/projects")
        return self

    @allure.step
    def is_loaded(self):
        expect(self.page.locator(".common-flash-success", has_text='Signed in successfully')).to_be_visible(
            timeout=15000)

    @allure.step
    def should_be_loaded(self):
        self.header.should_be_loaded()
        expect(self.grid).to_be_visible()
        expect(self.project_cards.first).to_be_visible()

    @allure.step
    def get_projects_count(self) -> int:
        return self.project_cards.count()

    @allure.step
    def get_all_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self.project_cards.all()]

    @allure.step
    def get_project_by_index(self, index: int) -> ProjectCard:
        return ProjectCard(self.project_cards.nth(index))

    @allure.step
    def get_project_by_name(self, name: str) -> ProjectCard:
        card = self.project_cards.filter(
            has=self.page.locator("h3", has_text=name)
        ).first

        return ProjectCard(card)

    @allure.step
    def should_have_project(self, name: str):
        expect(
            self.project_cards.filter(
                has=self.page.locator("h3", has_text=name)
            )
        ).to_have_count(1)

    @allure.step
    def open_project(self, name: str):
        self.get_project_by_name(name).open()

    @allure.step
    def search_project(self, text: str):
        self.header.search(text)

    @allure.step
    def should_have_projects_count(self, expected: int):
        expect(self.project_cards).to_have_count(expected)

    @allure.step
    def should_show_success_message(self, text: str):
        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_contain_text(text)

    @allure.step
    def should_show_info_message(self, text: str):
        expect(self.info_message).to_be_visible()
        expect(self.info_message).to_contain_text(text)
