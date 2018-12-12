from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackView.as_view(), name='feedback'),
    path('thanks',views.FeedbackView.as_view(), name='success'),
]