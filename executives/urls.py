from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'executive'

urlpatterns = [
    path('register', views.ExecutiveSignUpView.as_view(), name='register'),
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
    path('party-orders/all', views.PartyOrdersView.as_view(), name='all_party_orders'),
    path('party-orders/delete/<int:oid>', views.PartyOrderCancelView, name='cancel_party_order'),
    path('orders/<int:oid>', views.OrderView.as_view(), name='order'),
    path('orders/cancel/<int:oid>', views.CancelOrderView, name='cancel_order'),
    path('agent_applications', views.AgentApplicationsView.as_view(), name='agent_applications'),
    path('agent_applications/accept/<int:aid>', views.AcceptAgentApplication, name='accept_agent_appl'),
    path('agent_applications/reject/<int:aid>', views.RejectAgentApplication, name='reject_agent_appl'),
    path('support', views.SupportView.as_view(), name='support'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('subscriptions/create', views.SubscriptionCreateView.as_view(), name='create_subscription'),
    path('subscriptions/delete/<str:id>', views.SubscriptionDeleteView, name='deletesubscription'),
    path('notify-agent/<int:aid>', views.AgentNotifyView.as_view(), name='notify_agent'),
    path('feedback-view/all', views.FeedbackView.as_view(), name='feedback_all'),
    ]