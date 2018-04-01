
from selenium import webdriver
import unittest

class Functional_Test(unittest.TestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_headless()
        self.browser = webdriver.Firefox(options=firefox_options)

    def test_open_index_page(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("To-do", self.browser.title)

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main(warnings='ignore')
