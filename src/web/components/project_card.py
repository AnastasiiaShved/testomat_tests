from playwright.sync_api import Locator, expect


class ProjectCard:
    def __init__(self, card: Locator):
        self.card = card
        self.link = card.locator("a")
        self.title = card.locator("h3")
        self.tests = card.locator("p.text-gray-500")
        self.badges = card.locator(".project-badges span")
        self.avatars = card.locator("img.rounded-full")
        self.extra_users = card.locator("div.rounded-full.text-xs")

    def open(self):
        self.link.click()

    def get_title(self) -> str:
        return self.title.inner_text()

    def should_have_title(self, name: str):
        expect(self.title).to_have_text(name)

    def get_tests_count_text(self) -> str:
        return self.tests.inner_text()

    def get_tests_count(self) -> int:
        text = self.get_tests_count_text()
        return int(text.split()[0])

    def should_have_tests(self, expected: int):
        expect(self.tests).to_have_text(f"{expected} tests")

    def get_badges(self) -> list[str]:
        return self.badges.all_inner_texts()

    def should_have_badge(self, text: str):
        expect(self.badges.filter(has_text=text)).to_be_visible()

    def badges_count(self) -> int:
        return self.badges.count()

    def get_avatars_count(self) -> int:
        return self.avatars.count()

    def get_extra_users_count(self) -> int:
        if self.extra_users.count() == 0:
            return 0

        text = self.extra_users.inner_text()  # "+72"
        return int(text.replace("+", ""))

    def should_have_avatars(self, count: int):
        expect(self.avatars).to_have_count(count)
