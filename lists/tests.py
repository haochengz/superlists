from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item


class ListViewTest(TestCase):

    def test_home_page_display_multiple_items(self):
        Item.objects.create(text="Item 1")
        Item.objects.create(text="Item 2")

        response = self.client.get('/lists/only_list/')

        self.assertContains(response=response, text='Item 1')
        self.assertContains(response=response, text='Item 2')

    def test_uses_list_template(self):
        resp = self.client.get('/lists/only_list/')

        self.assertTemplateUsed(resp, 'list.html')

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

    def test_home_page_can_save_a_POST_request_to_db(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "Adding a new to-do item"

        response = home_page(request)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, request.POST['item_text'])

    def test_home_page_submit_a_POST_then_redirects_to_index(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "Adding a new to-do item"

        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/only_list/')

    def test_home_page_only_saves_item_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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
