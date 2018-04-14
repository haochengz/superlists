
from unittest import skip

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_item(self):
        self.browser.get(self.live_server_url)
        self.submit_a_item_at_index_page("")
        # 前端禁止了提交空输入
        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, "You can't have an empty list item") 

        self.submit_a_item_at_index_page("Buy some fresh milk")
        self.check_for_row_of_table_contains_item("1: Buy some fresh milk")
        
        self.submit_a_item_at_index_page("")
        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, "You can't have an empty list item") 

        self.submit_a_item_at_index_page("Make a cup of tea")
        self.check_for_row_of_table_contains_item("2: Make a cup of tea")

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.submit_a_item_at_index_page("Buy wellies")
        self.check_for_row_of_table_contains_item("1: Buy wellies")

        self.submit_a_item_at_index_page("Buy wellies")
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list") 
        
