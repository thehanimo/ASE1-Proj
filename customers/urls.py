from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'customer'

urlpatterns = [
	path('home', views.HomeView, name='home'),
    path('home/myorders', views.MyOrdersView.as_view(), name='myorders'),
    path('home/myorders/<int:oid>', views.OrderView.as_view(), name='order'),
    path('home/myorders/track/', views.orderTrack, name='order_track'),
    path('home/myorders/cancel/<int:oid>', views.CancelOrderView, name='cancel_order'),
    path('profile/edit', views.CustomerDetailsView.as_view(), name='editprofile'),
    path('profile/new', views.NewCustomerDetailsView.as_view(), name='newprofile'),
    path('support', views.support, name='support'),
    path('party-orders', views.PartyOrderCreateView.as_view(), name='party_order'),
    path('party-orders/success', views.PartyOrderCreateView.as_view(), name='party_orders_success'),
    path('subscriptions', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('home/mysubscriptions', views.MySubscriptionsView.as_view(), name='my_subscriptions'),
    path('home/mysubscriptions/<int:id>', views.SubscriptionClaimView, name='claim_subscription'),
    ]