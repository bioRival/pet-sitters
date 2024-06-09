from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views
from .views import ServicesList, PetCreate, PetUpdate, PetDelete
from django.conf.urls.static import static


urlpatterns = [
    path('', ServicesList.as_view(), name='home'), # домашняя страница
    path('pet_create/', PetCreate.as_view(), name='pet_create'),
    path('<int:pk>/update/', PetUpdate.as_view(), name='pet_update'),
    path('<int:pk>/delete/', PetDelete.as_view(), name='pet_delete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ссылка для выхода {% url 'user_app:logout' %}
# ссылка для входа {% url 'user_app:login' %}
