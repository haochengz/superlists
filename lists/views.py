from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

import time


def home_page(request):
    return render(request, 'lists_index.html')

def view_list(request):
    items = Item.objects.all()
    returt render(request, 'list.html', {'items': items})

def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('item_text', ''), saving_list=list_)
        return redirect('/lists/only_list/')
