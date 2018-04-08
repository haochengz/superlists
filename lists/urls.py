
from django.urls import path
from django.conf.urls import url

from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
    url(r'^lists/(\d+)/add$', views.add_item, name='add_item'),
    url(r'^lists/new$', views.new_list, name='new_list'),
]