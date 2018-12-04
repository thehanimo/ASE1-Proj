from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'customer'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
    path('home/myorders', views.MyOrdersView.as_view(), name='myorders'),
    path('home/myorders/<int:oid>', views.OrderView.as_view(), name='order'),
    path('home/myorders/track/<int:oid>', views.orderTrack, name='order_track'),
    path('home/myorders/cancel/<int:oid>', views.CancelOrderView, name='cancel_order'),
    path('profile/edit', views.CustomerDetailsView.as_view(), name='editprofile'),
    path('profile/new', views.NewCustomerDetailsView.as_view(), name='newprofile'),
    path('support', views.support, name='support')
    ]