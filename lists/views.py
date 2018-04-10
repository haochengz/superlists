
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError


from lists.models import Item, List


def home_page(request):
    return render(request, 'lists_index.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], saving_list=list_)
        return redirect('/lists/%d/' % list_.id)
    items = Item.objects.filter(saving_list=list_)
    return render(request, 'list.html', {'items': items, 'list': list_})

def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        item = Item(text=request.POST.get('item_text', ''), saving_list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            list_.delete()
            error = "You can't have an empty list item"
            return render(request, 'lists_index.html', {'error': error} )
        return redirect('/lists/%d/' % list_.id)
