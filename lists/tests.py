from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
import string

from lists.views import home_page, new_list, view_list

# Create your tests here.
class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница возвращает правильный html'''
        response = self.client.get('/')
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_item(self):
        '''тест сохранения и получения элементов списка'''
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list1 = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list1 = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list1, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list1, list_)

class ListViewTest(TestCase):
    """тест представления списка"""

    
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):   
        '''тест: отображаются все элементы списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='Itemey 1', list1=correct_list)
        Item.objects.create(text='Itemey 2', list1=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='другой элемент 1 списка', list1=other_list)
        Item.objects.create(text='другой элемент 2 списка', list1=other_list)


        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')
        self.assertNotContains(response, 'другой элемент 1 списка')
        self.assertNotContains(response, 'другой элемент 2 списка')


    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить POST запрос'''
        response = self.client.post('/list/new', data={'item_text' : 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''тест: переадресует после post-запроса'''
        response = self.client.post('/list/new', data={'item_text' : 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_passes_correct_list_to_template(self):
        '''тест: передается правильный шаблон списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewItemTest(TestCase):
    '''тест нового элемента списка'''
    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно сохранить post-запрос в существующий список'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list1, correct_list)

    def test_redirects_to_list_view(self):
        '''тест: переадресуется в представление списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')


    
    


