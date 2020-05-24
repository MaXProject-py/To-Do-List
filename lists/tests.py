from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item
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

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить POST запрос'''
        response = self.client.post('/', data={'item_text' : 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''тест: переадресует после post-запроса'''
        response = self.client.post('/', data={'item_text' : 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/new_list/')

    def test_only_saves_item_when_nessesary(self):
        '''тест: сохраняет элементы только когда нужно'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_item(self):
        '''тест сохранения и получения элементов списка'''
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):
    """тест представления списка"""

    
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        response = self.client.get('/lists/new_list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_item(self):   
        '''тест: отображаются все элементы списка'''

        Item.objects.create(text='Itemey 1')
        Item.objects.create(text='Itemey 2')

        response = self.client.get('/lists/new_list/')

        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')


