
from unittest import skip

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_item(self):
        self.browser.get(self.live_server_url)
        self.submit_a_item_at_index_page("")
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item") 

        self.submit_a_item_at_index_page("Buy some fresh milk")
        self.check_for_row_of_table_contains_item("1: Buy some fresh milk")
        
        self.submit_a_item_at_index_page("")
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item") 

        self.submit_a_item_at_index_page("Make a cup of tea")
        self.check_for_row_of_table_contains_item("1: Make a cup of tea")
