from django.urls import include, path

from .views import userAuth
import agents.views as agents
import customers.views as customers
import executives.views as executives

from django.conf.urls import url
urlpatterns = [
    path('', userAuth.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', customers.activate, name='activate'),
    url(r'^executive/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', executives.activate, name='exec_activate'),
    url(r'^accounts/NewPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', agents.activate, name='agent_activate'),
]
