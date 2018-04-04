
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class Functional_Test(unittest.TestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_headless()
        self.browser = webdriver.Firefox(options=firefox_options)
        self.browser.implicitly_wait(3)

    def test_open_index_page(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("to-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('to-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item',
                )
        inputbox.send_keys('Buy peacook feathers')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Buy peacook feathers' for row in rows),
                "New to-do item didn't appear in to-do list table.",
                )

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main()
