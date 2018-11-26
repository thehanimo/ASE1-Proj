from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'agent'

urlpatterns = [
	path('home', views.HomeView, name='home'),
    path('profile/view/<int:aid>', views.AgentDetailsView, name='viewprofile'),
    path('orders/<int:oid>', views.OrderView.as_view(), name='order'),
    path('orders/incoming', views.IncomingOrdersView.as_view(), name='incomingorders'),
    path('orders/assigned', views.AssignedOrdersView.as_view(), name='assignedorders'),
    path('orders/completed', views.CompletedOrdersView.as_view(), name='completedorders'),
    path('home/cancelled/cancelled', views.CancelledOrdersView.as_view(), name='cancelledorders'),
    path('home/incomingorders/accept/<int:oid>', views.AcceptOrderView, name='accept_order'),
    path('home/incomingorders/cancel/<int:oid>', views.CancelOrderView, name='cancel_order'),
    path('home/incomingorders/outfordelivery/<int:oid>', views.OutForDeliveryOrderView, name='outfordelivery_order'),
    path('home/incomingorders/delivered/<int:oid>', views.DeliveredOrderView, name='delivered_order'),
    ]