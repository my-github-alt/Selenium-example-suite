#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ./pageobjects/login.py

# built-in imports
from typing import Union

import logging
from urllib.parse import urljoin

# third-party imports
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException


logger = logging.getLogger(__name__)

# XPath's
INPUT = "//input[@id='{id}']"   # Reusable with str's .format function
SUBMIT = "//button[contains(@class, 'btn')]"
ERR_MSG = "//div[contains(@class, 'alert-danger')]"


class Login:
    # url with login box
    base_url = r'http://demostore.gatling.io/'
    login_url = urljoin(base_url, 'login')

    def __init__(self, driver: WebDriver, username: str, password: str) -> None:
        logger.debug('Login.username = %s' % str(username))
        logger.debug('Login.password = %s' % str(password))
        self.driver = driver
        self.password = password
        self.username = username

    def __locate(self, xpath: str, timeout: int = 10) -> WebElement:
        """private function, reusable code
        can raise `TimeoutException`
        """
        logger.debug('locate XPath: %s' % xpath)
        locator: tuple = (By.XPATH, xpath)
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def __insert(self, xpath: str, keys: str, timeout: int = 10) -> WebElement:
        """private function, reusable code"""
        we: WebElement = self.__locate(xpath, timeout)
        # we: WebElement = self.driver.find_element(By.XPATH, xpath)  # no polling-wait, can fail
        we.clear()
        we.send_keys(keys)
        return we

    def insert_username(self, username: str = None) -> None:
        """write text into the input of: Username"""
        username = username if username is not None else self.username   # ternary if-statement
        xpath = INPUT.format(id='username')
        self.__insert(xpath, username)
        logger.info('username is set to: %s' % username)

    def insert_password(self, password: str = None) -> None:
        """write text into the input of: Password"""
        password = password if password is not None else self.password   # ternary if-statement
        xpath = INPUT.format(id='password')
        self.__insert(xpath, password)
        logger.info('password is set to: %s' % password)

    def submit(self) -> None:
        """click the Login button"""
        self.__locate(xpath=SUBMIT).click()
        logger.info('pressed submit')

    def error_message(self, timeout: int = 3) -> Union[str, None]:
        """get the error message text or `None`"""
        errmsg = None
        try:
            errmsg = self.__locate(xpath=ERR_MSG, timeout=timeout).text
            logger.debug('error message on screen: %s' % errmsg)
        except WebDriverException:
            logger.debug('no error message on screen')
        finally:
            return errmsg  # -> str or None


if __name__ == '__main__':
    # local test
    from src.browser import get_driver  # local import from ./src/

    # basic logger
    logging.basicConfig(level=logging.DEBUG)

    driver = get_driver(browser='chrome')  # open browser
    driver.get(Login.login_url)  # navigate to website

    # provide driver and valid credentials
    login = Login(driver, username='john', password='pass')
    login.insert_username()
    login.insert_password()
    login.submit()

    # driver.quit()  # stop browser
