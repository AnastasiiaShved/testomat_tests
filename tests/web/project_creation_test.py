from faker import Faker

from src.web.application import Application


def test_new_project_creation(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .submit_project_create())

    (logged_app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (logged_app.project_page
     .side_bar
     .is_loaded()
     .is_active('Tests'))
