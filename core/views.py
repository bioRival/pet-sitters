from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Services
from .serializers import ServicesSerializer


class ServicesAPIView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

def index(request):
    return render(request, "home.html")
