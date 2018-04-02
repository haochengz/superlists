from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page

# Create your tests here.

class Test(TestCase):

    def test_home_page_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_response(self):
        req = HttpRequest()
        resp = home_page(req)
        self.assertTrue(resp.content.strip().startswith(b"<html>"))
        self.assertIn(b"<title>One to-do list</title>", resp.content)
        self.assertTrue(resp.content.strip().endswith(b"</html>"))
        
