from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
	path('', views.inp, name='api'),
]

