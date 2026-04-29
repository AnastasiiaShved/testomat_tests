from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.base_page import BasePage


class ProjectsPage(BasePage):
    PATH = "/projects"

    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".common-flash-success")
    INFO_MESSAGE = (By.CSS_SELECTOR, ".common-flash-info")
    GRID = (By.CSS_SELECTOR, "#grid")
    PROJECT_CARDS = (By.CSS_SELECTOR, "#grid li")
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search")

    def __init__(self, driver: WebDriver, base_url: str = ""):
        super().__init__(driver)
        self._base_url = base_url

    def open(self) -> None:
        self.driver.get(f"{self._base_url}{self.PATH}")

    def is_loaded(self) -> None:
        self.wait.for_visible(self.SUCCESS_MESSAGE)

    def should_be_loaded(self) -> None:
        self.wait.for_visible(self.GRID)
        cards = self.find_all(self.PROJECT_CARDS)
        assert len(cards) > 0, "No project cards found on the page"

    def get_projects_count(self) -> int:
        return len(self.find_all(self.PROJECT_CARDS))

    def get_all_projects(self) -> list[WebElement]:
        return self.find_all(self.PROJECT_CARDS)

    def get_project_by_index(self, index: int) -> WebElement:
        return self.find_all(self.PROJECT_CARDS)[index]

    def get_project_by_name(self, name: str) -> WebElement:
        cards = self.find_all(self.PROJECT_CARDS)
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, "h3")
            if title.text == name:
                return card
        raise ValueError(f"Project '{name}' not found")

    def should_have_project(self, name: str) -> None:
        self.get_project_by_name(name)

    def open_project(self, name: str) -> None:
        card = self.get_project_by_name(name)
        card.find_element(By.CSS_SELECTOR, "a").click()

    def search_project(self, text: str) -> None:
        self.type(self.SEARCH_INPUT, text)

    def should_have_projects_count(self, expected: int) -> None:
        actual = self.get_projects_count()
        assert actual == expected, f"Expected {expected} projects, got {actual}"

    def should_show_success_message(self, text: str) -> None:
        element = self.wait.for_visible(self.SUCCESS_MESSAGE)
        assert text in element.text, f"Expected '{text}' in success message, got '{element.text}'"

    def should_show_info_message(self, text: str) -> None:
        element = self.wait.for_visible(self.INFO_MESSAGE)
        assert text in element.text, f"Expected '{text}' in info message, got '{element.text}'"
