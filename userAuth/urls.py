from django.urls import include, path

from .views import userAuth, agents, customers, executives

urlpatterns = [
    path('', userAuth.home, name='home'),

    path('agent/home', include(([
        path('', agents.HomeView.as_view(), name='home'),
    ], 'userAuth'), namespace='agent')),

    path('home', include(([
        path('', customers.HomeView.as_view(), name='home'),
    ], 'userAuth'), namespace='customer')),

    path('executive/home', include(([
        path('', executives.HomeView.as_view(), name='home'),
    ], 'userAuth'), namespace='executive')),

]
