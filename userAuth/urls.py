from django.urls import include, path

from .views import userAuth, agents, customers, executives

urlpatterns = [
    path('', userAuth.home, name='home'),

    path('agent/', include(([
        path('home', agents.HomeView.as_view(), name='home'),
    ], 'userAuth'), namespace='agent')),

    path('', include(([
        path('home', customers.HomeView.as_view(), name='home'),
        path('profile/edit', customers.CustomerDetailsView.as_view(), name='editprofile'),
        path('profile/new', customers.NewCustomerDetailsView.as_view(), name='newprofile'),
    ], 'userAuth'), namespace='customer')),

    path('executive/', include(([
        path('home', executives.HomeView.as_view(), name='home'),
    ], 'userAuth'), namespace='executive')),

]
