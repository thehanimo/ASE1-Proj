from django.conf.urls import include, url
from . import views

app_name = 'paytm'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^payment/', views.payment, name='payment'),
    url(r'^response/', views.response, name='response'),
    url(r'^status/', views.status, name='status'),
]