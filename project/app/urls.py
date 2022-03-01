
from ipaddress import ip_address
from unicodedata import name
from xml.dom.minidom import Document
from django.urls import path,include
from . import views



urlpatterns = [

    path('',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('update_Item',views.UpdateItem, name='updat_item'),
    path('process_order/',views.ProcessOrder, name='process_order')
]

