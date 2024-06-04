from django.urls import path
from django.contrib.auth import views as auth_views
from user_app import views
from user_app.views import LogoutView

app_name = 'user_app'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
]
