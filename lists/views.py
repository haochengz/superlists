from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        return render(
                request, 
                'lists_index.html', 
                {
                    "new_item_text":request.POST.get('item_text', ''),
                }
            )
    return render(request, 'lists_index.html')
