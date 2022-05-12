#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ./test/website_login_test.py

# built-in imports
import json
import unittest
from importlib.resources import open_text
from types import SimpleNamespace

# third-party imports
from selenium.webdriver.remote.webdriver import WebDriver

# local imports
from src.browser import get_driver
from pageobjects.login import Login

# open and read the ./config/test_config.json
# use SimpleNamespace to access the json values using dot notation instead of dict
configuration = json.load(
    open_text("config", "test_config.json"),  # importlib.resources
    object_pairs_hook=lambda pairs: SimpleNamespace(**dict(pairs))
)


class WebsiteLoginTest(unittest.TestCase):
    """test the login using the `Login` class from pageobjects module"""
    driver: WebDriver

    @classmethod
    def setUpClass(cls) -> None:
        """do at start of the test"""
        cls.driver = get_driver(
            browser=configuration.browser_name,
            install_dir=configuration.driver_install_dir,
            headless=configuration.headless,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """do at end of the test"""
        cls.driver.quit()   # stop the browser

    def setUp(self) -> None:
        """do before each testcase"""
        self.driver.get(Login.login_url)  # navigate to login url
        self.login = Login(
            self.driver,
            username=configuration.valid_username,
            password=configuration.valid_password
        )

    def tearDown(self) -> None:
        """do after each testcase"""
        self.driver.delete_all_cookies()
        # javascript
        self.driver.execute_script("""window.localStorage.clear()""")
        self.driver.execute_script("""window.sessionStorage.clear()""")

    def test_no_unexpected_redirect(self):
        expected = Login.login_url
        received = self.driver.current_url
        self.assertEqual(expected, received, msg='url is not the same')

    def test_error_no_username(self):
        expected = 'Invalid credentials'
        self.login.insert_password()  # enter password
        self.login.submit()           # click login button
        received = self.login.error_message()
        self.assertEqual(expected, received, msg='expected error message: %s' % expected)

    def test_error_no_password(self):
        expected = 'Invalid credentials'
        self.login.insert_username()  # enter username
        self.login.submit()           # click login button
        received = self.login.error_message()
        self.assertEqual(expected, received, msg='expected error message: %s' % expected)

    def test_error_invalid_credentials(self):
        expected = 'Invalid credentials'
        self.login.insert_username()  # enter username and password
        self.login.insert_password(password='Wrong password')
        self.login.submit()           # click login button
        received = self.login.error_message()
        self.assertEqual(expected, received, msg='expected error message: %s' % expected)

    def test_no_error_when_valid_login(self):
        expected = None  # Login.error_message returns `None` if no error is found
        self.login.insert_username()  # enter username and password
        self.login.insert_password()
        self.login.submit()           # click login button
        received = self.login.error_message(timeout=5)
        self.assertIs(expected, received, msg='received error message %s' % str(received))

    def test_valid_login(self):
        expected = Login.base_url  # url after login
        self.login.insert_username()  # enter username and password
        self.login.insert_password()
        self.login.submit()           # click login button
        received = self.driver.current_url
        self.assertEqual(expected, received, msg='url is not the same')


if __name__ == '__main__':
    # local test
    import logging
    logging.basicConfig(level=logging.DEBUG)

    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None  # uncomment for sequential test execution
    suite = loader.loadTestsFromTestCase(WebsiteLoginTest)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(suite)
