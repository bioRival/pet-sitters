from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import ServicesList, BaseRegisterView

urlpatterns = [
    path('', ServicesList.as_view(), name='services_list'), # домашняя страница
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    # path("customer_profile/", views.customer_profile, name="customer_profile"),
]
