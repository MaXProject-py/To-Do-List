from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item
# Create your views here.
def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html')

def view_list(request):
    '''представлениие списка'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items' : items})

def new_list(request):
    '''новый список'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/new_list/')