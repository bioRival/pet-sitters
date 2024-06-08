from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views
from .views import ServicesList, CustomerProfile, ShowProfilePageView, CreateProfilePageView
from django.conf.urls.static import static

urlpatterns = [
    path('', ServicesList.as_view(), name='home'), # домашняя страница
    path("customer_profile/<str:slug>/", CustomerProfile.as_view(), name="customer_profile"),
    path("profile/", views.customer_profile, name="profile"),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_user_profile'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ссылка для выхода {% url 'user_app:logout' %}
# ссылка для входа {% url 'user_app:login' %}
