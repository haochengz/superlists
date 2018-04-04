from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item

# Create your tests here.

class TestViews(TestCase):

    def test_home_page_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_response(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8").strip()
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>One to-do list</title>", html)
        self.assertTrue(html.endswith("</html>"))

    def test_home_page_post_new_item(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "Adding a new to-do item"

        response = home_page(request)
        html = response.content.decode()
        self.assertIn("Adding a new to-do item", html)


class TestModels(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first = saved_items[0]
        second = saved_items[1]
        self.assertEqual(first.text, first_item.text)
        self.assertEqual(second.text, second_item.text)
