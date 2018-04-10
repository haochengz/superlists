
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List


class TestHomepageViews(TestCase):
    """
    Views: home_page
    """
    def test_home_page_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_response(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8").strip()
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>One to-do list</title>", html)
        self.assertTrue(html.endswith("</html>"))


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/%d/add' % correct_list.id,
                data = {
                    'item_text': 'Add a new item to existing list'
                }
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Add a new item to existing list')
        self.assertEqual(new_item.saving_list, correct_list)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        resp = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(resp.context['list'], correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        resp = self.client.post(
                '/lists/%d/add' % correct_list.id,
                data = {
                    'item_text': 'Add a new item to existing list'
                }
            )

        self.assertRedirects(resp, '/lists/%d/' % correct_list.id)


class ListViewTest(TestCase):
    def test_home_page_display_multiple_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="Item 1", saving_list=list_)
        Item.objects.create(text="Item 2", saving_list=list_)
        new_list = List.objects.first()

        response = self.client.get('/lists/%d/' % new_list.id)

        self.assertContains(response=response, text='Item 1')
        self.assertContains(response=response, text='Item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        resp = self.client.get('/lists/%d/' % list_.id)

        self.assertTemplateUsed(resp, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', saving_list=correct_list)
        Item.objects.create(text='Item 2', saving_list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Item 3', saving_list=other_list)
        Item.objects.create(text='Item 4', saving_list=other_list)

        resp = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(resp, 'Item 1')
        self.assertContains(resp, 'Item 2')
        self.assertNotContains(resp, 'Item 3')
        self.assertNotContains(resp, 'Item 4')

    def test_home_page_can_save_a_POST_request_to_db(self):
        self.client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_submit_a_POST_then_redirect(self):
        response = self.client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
            )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.id)


