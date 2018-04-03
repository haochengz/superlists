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
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8").strip()
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>One to-do list</title>", html)
        self.assertTrue(html.endswith("</html>"))
        
