from django.urls import include, path

from .views import userAuth, agents, customers, executives

from django.conf.urls import url
urlpatterns = [
    path('', userAuth.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', customers.activate, name='activate'),
    url(r'^executive/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', executives.activate, name='exec_activate'),
    url(r'^accounts/NewPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', agents.activate, name='agent_activate'),

    path('agent/', include(([
        path('home', agents.HomeView, name='home'),
        path('register', agents.AgentSignUp, name='register'),
        path('profile/view/<int:aid>', agents.AgentDetailsView, name='viewprofile'),
        path('orders/incoming', agents.IncomingOrdersView.as_view(), name='incomingorders'),
        path('orders/assigned', agents.AssignedOrdersView.as_view(), name='assignedorders'),
        path('orders/completed', agents.CompletedOrdersView.as_view(), name='completedorders'),
        path('home/cancelled/cancelled', agents.CancelledOrdersView.as_view(), name='cancelledorders'),
        path('home/incomingorders/accept/<int:oid>', agents.AcceptOrderView, name='accept_order'),
        path('home/incomingorders/cancel/<int:oid>', agents.CancelOrderView, name='cancel_order'),
        path('home/incomingorders/outfordelivery/<int:oid>', agents.OutForDeliveryOrderView, name='outfordelivery_order'),
        path('home/incomingorders/delivered/<int:oid>', agents.DeliveredOrderView, name='delivered_order'),
    ], 'userAuth'), namespace='agent')),

    path('', include(([
        path('home', customers.HomeView.as_view(), name='home'),
        path('home/myorders', customers.MyOrdersView.as_view(), name='myorders'),
        path('home/myorders/<int:oid>', customers.OrderView.as_view(), name='order'),
        path('home/myorders/cancel/<int:oid>', customers.CancelOrderView, name='cancel_order'),
        path('profile/edit', customers.CustomerDetailsView.as_view(), name='editprofile'),
        path('profile/new', customers.NewCustomerDetailsView.as_view(), name='newprofile'),
    ], 'userAuth'), namespace='customer')),

    path('executive/', include(([
        path('register', executives.ExecutiveSignUpView.as_view(), name='register'),
        path('home', executives.HomeView.as_view(), name='home'),
        path('profile/view', executives.ExecutiveDetailsView.as_view(), name='viewprofile'),
        path('agents_view', executives.AgentsView.as_view(), name='agentslist'),
        path('agent_profile/<int:aid>', agents.AgentDetailsView, name='viewagentprofile'),
        path('agent_edit/<str:id>', executives.AgentEditView, name='editagent'),
        path('agent_delete/<str:id>', executives.AgentDeleteView, name='deleteagent'),
        path('category/create', executives.CategoryCreateView.as_view(), name='create_category'),
        path('categories/', executives.CategoriesView.as_view(), name='category'),
        path('product/create', executives.ProductCreateView.as_view(), name='create_product'),
        path('products/', executives.ProductsView.as_view(), name='product'),
        path('product/edit/<int:pid>', executives.ProductDetailsView.as_view(), name='editproduct'),
        path('product/delete/<str:id>', executives.ProductDeleteView, name='deleteproduct'),
        path('category/delete/<str:id>', executives.CategoryDeleteView, name='deletecategory'),
        path('orders/all', executives.AllOrdersView.as_view(), name='all_orders'),
        path('orders/<int:oid>', customers.OrderView.as_view(), name='order'),
        path('orders/cancel/<int:oid>', agents.CancelOrderView, name='cancel_order'),
    ], 'userAuth'), namespace='executive')),

]
