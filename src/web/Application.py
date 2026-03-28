from playwright.sync_api import Page

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.NewProjects import NewProjectsPage
from src.web.pages.ProjectPage import ProjectPage
from src.web.pages.ProjectsPage import ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_project_page = NewProjectsPage(page)
        self.project_page = ProjectPage(page)
