from django.urls import path
from . import views
from .views import ServicesList

urlpatterns = [
    path('', ServicesList.as_view(), name='services_list'), # домашняя страница
]