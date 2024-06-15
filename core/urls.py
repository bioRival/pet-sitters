from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views
from .views import ServicesList, PetCreate, PetUpdate, PetDelete, AddService, ServiceDelete, SittersList, SitterCard
from django.conf.urls.static import static


urlpatterns = [
    # домашняя страница
    path('', ServicesList.as_view(), name='home'),
    # каталог страница               
    path('search/', views.SearchSitters.as_view(), name='search'),    
    path('pets/pet_create/', PetCreate.as_view(), name='pet_create'),
    path('pets/<int:pk>/update/', PetUpdate.as_view(), name='pet_update'),
    path('pets/<int:pk>/delete/', PetDelete.as_view(), name='pet_delete'),
    path('service/add_service/', AddService.as_view(), name='add_service'),
    path('service/<int:pk>/delete/', ServiceDelete.as_view(), name='service_delete'),
    path('sitters/', (SittersList.as_view()), name='sitters_list'),
    path('sitters/<int:pk>', SitterCard.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ссылка для выхода {% url 'user_app:logout' %}
# ссылка для входа {% url 'user_app:login' %}
