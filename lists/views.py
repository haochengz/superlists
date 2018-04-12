
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError


from lists.models import Item, List
from lists.forms import ItemForm


def home_page(request):
    return render(request, 'lists_index.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], saving_list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
    items = Item.objects.filter(saving_list=list_)
    return render(request, 'list.html',
            {
                'items': items,
                'list': list_,
                'error': error,
                'form': ItemForm(),
            })

def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        item = Item(text=request.POST.get('text', ''), saving_list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            list_.delete()
            error = "You can't have an empty list item"
            return render(request, 'lists_index.html', {'error': error} )
        return redirect(list_)
