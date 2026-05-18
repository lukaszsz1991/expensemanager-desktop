import sys
import os

TEST = True
TEST_ROLE_IS_ADMIN = False # USER lub ADMIN
ADMIN_LOGIN = "admin@example.com"
ADMIN_PASSWORD = "ES-Admin123#"
USER_LOGIN = "test1@example.com"
USER_PASSWORD = "Test1234!"
MINUTES_TO_LOGOUT = 15
SECONDS_TO_WARNING = 30
API_BASE_URL = "https://www.wydatkomat.tech/api"


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)