from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import ServicesList, BaseRegisterView, CustomerProfile

urlpatterns = [
    path('', ServicesList.as_view(), name='services_list'), # домашняя страница
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_profile/<int:pk>/", CustomerProfile.as_view(), name="customer_profile"),
    path("profile/", views.customer_profile, name="profile"),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
