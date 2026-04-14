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

    def is_loaded(self):
        expect(self.page.locator(".common-flash-success", has_text='Signed in successfully')).to_be_visible(
            timeout=15000)

    def should_be_loaded(self):
        self.header.should_be_loaded()
        expect(self.grid).to_be_visible()
        expect(self.project_cards.first).to_be_visible()

    def get_projects_count(self) -> int:
        return self.project_cards.count()

    def get_all_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self.project_cards.all()]

    def get_project_by_index(self, index: int) -> ProjectCard:
        return ProjectCard(self.project_cards.nth(index))

    def get_project_by_name(self, name: str) -> ProjectCard:
        card = self.project_cards.filter(
            has=self.page.locator("h3", has_text=name)
        ).first

        return ProjectCard(card)

    def should_have_project(self, name: str):
        expect(
            self.project_cards.filter(
                has=self.page.locator("h3", has_text=name)
            )
        ).to_have_count(1)

    def open_project(self, name: str):
        self.get_project_by_name(name).open()

    def search_project(self, text: str):
        self.header.search(text)

    def should_have_projects_count(self, expected: int):
        expect(self.project_cards).to_have_count(expected)

    def should_show_success_message(self, text: str):
        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_contain_text(text)

    def should_show_info_message(self, text: str):
        expect(self.info_message).to_be_visible()
        expect(self.info_message).to_contain_text(text)
