
from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    def test_open_index_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("to-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        # 打开首页后标题栏中应当有to-do字样
        self.assertIn('to-do', header_text)

        inputbox = self.get_input_box()
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

        inputbox = self.get_input_box()
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
