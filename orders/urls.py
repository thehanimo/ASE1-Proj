from django.conf.urls import url
from . import views
from django.urls import path, include
from .models import Order

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^placed/(?P<uidb64>[0-9A-Za-z_\-]+)/', views.order_complete, name='order_complete'),
]