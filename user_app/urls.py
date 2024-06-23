from django.urls import path
from django.contrib.auth import views as auth_views
from user_app import views
from user_app.views import LogoutView

app_name = 'user_app'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.customer_signup, name='signup'),
    path('customer/<str:username>/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('sitter/<str:username>/', views.SitterProfileView.as_view(), name='sitter_profile'),
    path('<str:username>/settings/', views.UserSettingsView.as_view(), name='user_profile_settings'),
    path('customer/<str:username>/edit/', views.UserEditView.as_view(), name='user_profile_edit'),
    path('sitter/<str:username>/edit/', views.SitterEditView.as_view(), name='sitter_profile_edit'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
]
