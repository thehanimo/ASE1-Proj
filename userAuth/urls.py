from django.urls import include, path

from .views import userAuth, agents, customers, executives

from django.conf.urls import url
urlpatterns = [
    path('', userAuth.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', customers.activate, name='activate'),
    url(r'^executive/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', executives.activate, name='exec_activate'),

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
        path('profile/view', executives.ExecutiveDetailsView.as_view(), name='viewprofile'),
        path('register', executives.ExecutiveSignUpView.as_view(), name='register'),
    ], 'userAuth'), namespace='executive')),

]
