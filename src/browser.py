#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ./src/browser.py

# built-in imports
from typing import Literal

import logging
from pathlib import Path

# third-party imports
# selenium 4+
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
# selenium options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
# webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent

# collection of selenium supported browsers
BrowserName = Literal[
    'chrome',
    'chromium',
    'brave',
    'opera',
    'firefox',
    'edge',
    'ie'
]

logger = logging.getLogger(__name__)


def get_driver(browser: BrowserName, install_dir: str = None, headless: bool = False) -> WebDriver:
    """get the selenium driver of the given the browsers name"""

    # if `install_path` is `None` use ./src/ as driver install_path
    install_dir = str(THIS_DIR) if install_dir is None else install_dir
    if not Path(install_dir).is_dir() or not Path(install_dir).exists():
        logger.error('given install_dir is faulty: %s' % str(install_dir))
        logger.debug('revert to: %s' % str(THIS_DIR))
        install_dir = str(THIS_DIR)

    logger.debug('get browser: %s' % str(browser))
    logger.debug('headless: %s' % str(bool(headless)))
    logger.debug('driver download directory: %s' % str(install_dir))

    match browser:
        # Chromium based browsers
        case 'chrome':
            options = ChromeOptions()
            options.headless = bool(headless)
            service = Service(ChromeDriverManager(path=str(install_dir)).install())
            return webdriver.Chrome(service=service, options=options)
        case 'chromium':
            options = ChromeOptions()
            options.headless = bool(headless)
            service = Service(ChromeDriverManager(path=str(install_dir), chrome_type=ChromeType.CHROMIUM).install())
            return webdriver.Chrome(service=service, options=options)
        case 'brave':
            options = ChromeOptions()
            options.headless = bool(headless)
            service = Service(ChromeDriverManager(path=str(install_dir), chrome_type=ChromeType.BRAVE).install())
            return webdriver.Chrome(service=service, options=options)
        # Opera browser
        case 'opera':
            options = OperaOptions()
            options.headless = bool(headless)
            executable_path = OperaDriverManager(path=str(install_dir)).install()
            return webdriver.Opera(executable_path=executable_path, options=options)
        # Mozilla browser
        case 'firefox':
            options = FirefoxOptions()
            options.headless = bool(headless)
            service = Service(GeckoDriverManager(path=str(install_dir)).install())
            return webdriver.Firefox(service=service, options=options)
        # Windows browsers
        case 'edge':
            options = EdgeOptions()
            options.headless = bool(headless)
            service = Service(EdgeChromiumDriverManager(path=str(install_dir)).install())
            return webdriver.Edge(service=service, options=options)
        case 'ie':
            logger.warning('Stop using InternetExplorer')
            options = IEOptions()
            options.headless = bool(headless)
            service = Service(IEDriverManager(path=str(install_dir)).install())
            return webdriver.Ie(service=service, options=options)
        case _:
            logger.critical('unknown browser: %s' % str(browser))
            exit(1)
