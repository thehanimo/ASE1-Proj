from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
	path('track/agent/<int:oid>', views.inp, name='api'),
	path('track/get_coords/<int:oid>', views.out, name='coords_out'),
	path('poll', views.poll, name='poll'),

]

