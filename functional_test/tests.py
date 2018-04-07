
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

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
        time.sleep(2)
        table = self.browser.find_element_by_id('id_list_table')
        self.assertIn(row_text, 
                "".join([row.text for row in table.find_elements_by_tag_name('tr')]))

    def submit_a_item_at_index_page(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def test_open_index_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("to-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        # 打开首页后标题栏中应当有to-do字样
        self.assertIn('to-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        # 首页有输入栏且该输入栏是输入to-do item的输入栏
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item',
                )
        self.submit_a_item_at_index_page("Buy peacock feathers")
        # 提交一个item后将回显在首页上
        self.check_for_row_of_table_contains_item("1: Buy peacock feathers")

        self.submit_a_item_at_index_page("Use peacock feathers to make a fly")
        # 再次提交一个item将和之前的items一同回显在首页上
        # self.check_for_row_of_table_contains_item("1: Buy peacock feathers")
        self.check_for_row_of_table_contains_item("Use peacock feathers to make a fly")

        first_list_url = self.browser.current_url
        self.reset_browser()
        self.browser.get(self.live_server_url)
        html_body = self.browser.find_element_by_tag_name('body').text 
        # 启动新浏览器会话后前一个浏览器输入的内容将不能显示在新会话中
        self.assertNotIn("Buy peacock feathers", html_body)
        self.assertNotIn("make a fly", html_body)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.submit_a_item_at_index_page("Buy some milk")
        # 插入新数据后应当正常的回显
        self.check_for_row_of_table_contains_item("Buy some milk")

        new_list_url = self.browser.current_url
        # 新回话插入的新列表采用了新的URL地址
        self.assertRegex(new_list_url, '/lists/.+')
        self.assertNotEqual(new_list_url, first_list_url)

        html_body = self.browser.find_element_by_tag_name('body').text 
        # 前一个会话的输入依然不会显示出来
        self.assertNotIn("Buy peacock feathers", html_body)
        self.assertNotIn("make a fly", html_body)

    def tearDown(self):
        self.browser.close()

