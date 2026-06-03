import allure
from typing import Self

from playwright.sync_api import Page, expect

from src.web.pages.project_page import ProjectPage


class NewProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.__form_container = page.locator("#content-desktop form#new_project")

    @allure.step
    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    @allure.step
    def is_loaded(self) -> Self:
        expect(self.__form_container).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_contain_text('Classical')
        expect(self.__form_container.locator("#bdd")).to_be_visible()
        expect(self.__form_container.locator("#bdd")).to_contain_text('BDD')
        expect(self.__form_container.locator("#project_title")).to_be_visible()
        expect(self.__form_container.locator("#demo-btn")).to_be_visible()
        expect(self.__form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    @allure.step
    def fill_project_title(self, target_project_name: str) -> Self:
        self.__form_container.locator("#project_title").fill(target_project_name)
        return self

    @allure.step
    def submit_project_create(self) -> ProjectPage:
        self.__form_container.locator("input[type='submit'][value='Create']").click()
        return ProjectPage(self.page)

    @allure.step
    def click_create(self) -> ProjectPage:
        return self.submit_project_create()
