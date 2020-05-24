from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
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
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list1=list_)
    return redirect('/lists/new_list/')