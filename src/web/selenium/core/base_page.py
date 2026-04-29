from turtle import clear

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.waits import Wait, BySelector, SelectorElement


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = Wait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find(self, locator: BySelector) -> WebElement:
        return self.wait.for_present(locator)

    def find_all(self, locator: BySelector) -> list[WebElement]:
        return self.wait.for_all_present(locator)

    def click(self, target: SelectorElement) -> None:
        self.wait.for_clickable(target).click()

    def type(self, target: SelectorElement, text: str) -> None:
        element = self.wait.for_visible(target)
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    def clear_and_type(self, locator: BySelector, text: str) -> None:
        element = self.wait.for_visible(locator)
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator: BySelector) -> bool:
        try:
            return self.wait.for_visible(locator).is_displayed()
        except Exception:
            return False

    def is_present(self, locator: BySelector) -> bool:
        try:
            return self.wait.for_present(locator) is not None
        except Exception:
            return False

    def get_text(self, locator: BySelector) -> str:
        return self.wait.for_visible(locator).text

    def get_attribute(self, locator: BySelector, attribute: str) -> str:
        return self.wait.for_present(locator).get_attribute(attribute)
