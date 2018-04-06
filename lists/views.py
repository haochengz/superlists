from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

import time


def home_page(request):
    return render(request, 'lists_index.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect('/lists/only_list/')
