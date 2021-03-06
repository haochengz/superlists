
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.utils.html import escape
from unittest import skip
# from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
        ExistingListItemForm, ItemForm, 
        EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
    )


class TestHomepageViews(TestCase):

    def test_homepage_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_homepage_returns_correct_html(self):
        req = HttpRequest()
        resp = home_page(req)
        html = resp.content.decode("utf-8").strip()
        # expected_html = render_to_string('lists_index.html',{'form':ItemForm()})
        # self.assertMultiLineEqual(html, expected_html)
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>One to-do list</title>", html)
        self.assertTrue(html.endswith("</html>"))

    def test_homepage_renders_home_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'lists_index.html')

    def test_homepage_uses_item_form(self):
        resp = self.client.get('/')
        self.assertIsInstance(resp.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/%d/' % correct_list.id,
                data = {
                    'text': 'Add a new item to existing list'
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
        
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        resp = self.client.post(
                '/lists/%d/' % correct_list.id,
                data = {
                    'text': 'Add a new item to existing list'
                }
            )
        self.assertRedirects(resp, '/lists/%d/' % correct_list.id)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        resp = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(resp, 'list.html')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        resp = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(resp.context['form'], ExistingListItemForm)
        self.assertContains(resp, 'name="text"')

    def test_home_page_display_multiple_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="Item 1", saving_list=list_)
        Item.objects.create(text="Item 2", saving_list=list_)
        new_list = List.objects.first()
        response = self.client.get('/lists/%d/' % new_list.id)
        self.assertContains(response=response, text='Item 1')
        self.assertContains(response=response, text='Item 2')

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
                data={'text': 'A new list item'}
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_submit_a_POST_then_redirect(self):
        response = self.client.post(
                '/lists/new',
                data={'text': 'A new list item'}
            )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_for_invalid_input_passes_form_to_template(self):
        resp = self.client.post('/lists/new', data={'text': ""})
        self.assertIsInstance(resp.context['form'], ExistingListItemForm)

    def test_validation_errors_are_shown_on_homepage(self):
        resp = self.client.post('/lists/new', data={'text': ""})
        self.assertContains(resp, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_renders_homepage_template(self):
        resp = self.client.post('/lists/new', data={'text': ""})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lists_index.html')

    def test_empty_items_arent_saved(self):
        resp = self.client.post('/lists/new', data={'text': ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        resp = self.post_invalid_input()
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(resp, expected_error)
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_templates(self):
        resp = self.post_invalid_input()
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        resp = self.post_invalid_input()
        self.assertIsInstance(resp.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        resp = self.post_invalid_input()
        expected_error = escape("You can't have an empty list item")
        self.assertContains(resp, expected_error)

    def test_duplicate_item_shows_error_on_page(self):
        ls = List.objects.create()
        item = Item.objects.create(saving_list=ls, text='texts')
        resp = self.client.post(
                '/lists/%d/' % ls.id,
                data={'text': 'texts'}
            )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(resp, expected_error)
        self.assertTemplateUsed(resp, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
                '/lists/%d/' % list_.id,
                data={'text': ""},
            )


