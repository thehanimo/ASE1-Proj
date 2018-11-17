from django.urls import include, path

from .views import userAuth, agents, customers, executives

from django.conf.urls import url
urlpatterns = [
    path('', userAuth.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', customers.activate, name='activate'),
    url(r'^executive/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', executives.activate, name='exec_activate'),
    url(r'^accounts/NewPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', agents.activate, name='agent_activate'),

    path('agent/', include(([
        path('home', agents.HomeView.as_view(), name='home'),
        path('register', agents.AgentSignUp, name='register')
    ], 'userAuth'), namespace='agent')),

    path('', include(([
        path('home', customers.HomeView.as_view(), name='home'),
        path('profile/edit', customers.CustomerDetailsView.as_view(), name='editprofile'),
        path('profile/new', customers.NewCustomerDetailsView.as_view(), name='newprofile'),
        #path('shop', customers.ShopView.as_view(), name='shop')
    ], 'userAuth'), namespace='customer')),

    path('executive/', include(([
        path('home', executives.HomeView.as_view(), name='home'),
        path('profile/view', executives.ExecutiveDetailsView.as_view(), name='viewprofile'),
        path('register', executives.ExecutiveSignUpView.as_view(), name='register'),
        path('agentslist/view', executives.AgentsView.as_view(), name='agentslist'),
        path('agentedit/<str:id>', executives.AgentEditView, name='editagent'),
        path('agentdelete/<str:id>', executives.AgentDeleteView, name='deleteagent'),
    ], 'userAuth'), namespace='executive')),

]
