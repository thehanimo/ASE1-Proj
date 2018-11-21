from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'executive'

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/view', views.ExecutiveDetailsView.as_view(), name='viewprofile'),
    path('agents_view', views.AgentsView.as_view(), name='agentslist'),
    path('agent_profile/<int:aid>', views.AgentDetailsView, name='viewagentprofile'),
    path('agent_edit/<str:id>', views.AgentEditView, name='editagent'),
    path('agent_delete/<str:id>', views.AgentDeleteView, name='deleteagent'),
    path('category/create', views.CategoryCreateView.as_view(), name='create_category'),
    path('categories/', views.CategoriesView.as_view(), name='category'),
    path('product/create', views.ProductCreateView.as_view(), name='create_product'),
    path('products/', views.ProductsView.as_view(), name='product'),
    path('product/edit/<int:pid>', views.ProductDetailsView.as_view(), name='editproduct'),
    path('product/delete/<str:id>', views.ProductDeleteView, name='deleteproduct'),
    path('category/delete/<str:id>', views.CategoryDeleteView, name='deletecategory'),
    path('orders/all', views.AllOrdersView.as_view(), name='all_orders'),
    path('orders/<int:oid>', views.OrderView.as_view(), name='order'),
    path('orders/cancel/<int:oid>', views.CancelOrderView, name='cancel_order'),
    ]