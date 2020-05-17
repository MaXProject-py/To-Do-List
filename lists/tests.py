from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import string

from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница возвращает правильный html'''
        response = self.client.get('/') 
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        self.assertTemplateUsed(response, 'home.html')
