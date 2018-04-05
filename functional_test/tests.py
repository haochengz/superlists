
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class New_Visitor_Test(LiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_headless()
        self.browser = webdriver.Firefox(options=firefox_options)
        self.browser.implicitly_wait(3)

    def check_for_row_of_table_contains_item(self, row_text):
        # html文件再如不完整将引发selenium查找节点失败的错误
        time.sleep(2)
        table = self.browser.find_element_by_id('id_list_table')
        self.assertIn(row_text, 
                [row.text for row in table.find_elements_by_tag_name('tr')])

    def submit_a_item_at_index_page(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def test_open_index_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("to-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('to-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item',
                )
        self.submit_a_item_at_index_page("Buy peacock feathers")
        self.check_for_row_of_table_contains_item("1: Buy peacock feathers")

        self.submit_a_item_at_index_page("Use peacock feathers to make a fly")
        self.check_for_row_of_table_contains_item("1: Buy peacock feathers")
        self.check_for_row_of_table_contains_item("2: Use peacock feathers to make a fly")

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main()
