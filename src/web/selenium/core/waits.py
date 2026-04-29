from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BySelector = tuple[str, str]
SelectorElement = BySelector | WebElement

DEFAULT_TIMEOUT = 10
DEFAULT_POLL = 0.5
IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)


class Wait:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_POLL):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(
            driver,
            timeout,
            poll_frequency=DEFAULT_POLL,
            ignored_exceptions=IGNORED_EXCEPTIONS,
        )

    @staticmethod
    def _is_locator(target: SelectorElement) -> bool:
        return isinstance(target, tuple) and len(target) == 2

    def for_visible(self, target: SelectorElement, custom_timeout: int = None) -> WebElement:
        if custom_timeout:
            self._wait = WebDriverWait(self.driver, custom_timeout, poll_frequency=DEFAULT_POLL)
        if self._is_locator(target):
            return self._wait.until(EC.visibility_of_element_located(target))

        return self._wait.until(EC.visibility_of(target))

    def for_invisible(self, locator: BySelector) -> bool:
        return self._wait.until(EC.invisibility_of_element_located(locator))

    def for_present(self, locator: BySelector) -> WebElement:
        return self._wait.until(EC.presence_of_element_located(locator))

    def for_clickable(self, locator: BySelector) -> WebElement:
        return self._wait.until(EC.element_to_be_clickable(locator))

    def for_all_visible(self, locator: BySelector) -> list[WebElement]:
        return self._wait.until(EC.visibility_of_all_elements_located(locator))

    def for_all_present(self, locator: BySelector) -> list[WebElement]:
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def for_url_contains(self, text: str) -> bool:
        return self._wait.until(EC.url_contains(text))

    def for_url_matches(self, pattern: str) -> bool:
        return self._wait.until(EC.url_matches(pattern))

    def for_text_in_element(self, locator: BySelector, text: str) -> bool:
        return self._wait.until(EC.text_to_be_present_in_element(locator, text))
