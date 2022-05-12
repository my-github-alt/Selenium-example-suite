#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ./__main__.py

# built-in imports
import logging
import unittest

# local imports
from test.website_login_test import WebsiteLoginTest

if __name__ == '__main__':
    # local test
    logging.basicConfig(level=logging.DEBUG)

    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None  # uncomment for sequential test execution
    suite = loader.loadTestsFromTestCase(WebsiteLoginTest)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(suite)
