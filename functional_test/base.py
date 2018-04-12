
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = self.open_a_browser()

    def reset_browser(self):
        self.browser.quit()
        self.browser = self.open_a_browser()

    def open_a_browser(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_headless()
        browser = webdriver.Firefox(options=firefox_options)
        browser.implicitly_wait(3)
        return browser

    def check_for_row_of_table_contains_item(self, row_text):
        # html文件再如不完整将引发selenium查找节点失败的错误
        time.sleep(3)
        table = self.browser.find_element_by_id('id_list_table')
        self.assertIn(row_text, 
                "".join([row.text for row in table.find_elements_by_tag_name('tr')]))
    def submit_a_item_at_index_page(self, item_text):
        inputbox = self.get_input_box()
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def get_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def tearDown(self):
        self.browser.close()

