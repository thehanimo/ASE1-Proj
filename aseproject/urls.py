"""aseproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userAuth.views import userAuth
import agents.views as agents
import customers.views as customers
import executives.views as executives
from . import settings
from django.contrib.staticfiles.urls import static\
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('userAuth.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', customers.CustomerSignUpView.as_view(), name='signup'),
	path('accounts/iforgot/', userAuth.password_reset, name='password_reset'),
	url(r'^accounts/NewPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', userAuth.new_password, name='new_password'),
	path('accounts/changepassword', userAuth.change_password, name='change_password'),
    path('agent/', include('agents.urls')),
    path('customer/', include('customers.urls')),
    path('executive/', include('executives.urls')),
	path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('shop/', include('shop.urls')),
    path('api/', include('api.urls')),
    path('support/', include('chat.urls')),
    path('forbidden', userAuth.forbidden, name='forbidden'),
]
#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)