from django.urls import path, re_path
from . import views


app_name = 'chat'

urlpatterns = [
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('crumbs', views.error, name='support_error'),
    path('rainbows', views.success, name='support_success'),
]
