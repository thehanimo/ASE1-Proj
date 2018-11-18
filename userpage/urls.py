from django.urls import path,include
from . import views

app_name='userpage'

urlpatterns = [
    path('',views.userpage,name="userpage"),
    path('checkout/',views.checkout,name="checkout"),
    path('orders/',views.yourorders,name="yourorders"),
    path('orderplaced/',views.orderplaced,name="orderplaced"),
    path('notifications/',views.notifications,name="notifications"),
]
