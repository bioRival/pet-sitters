from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from rest_framework import generics

from . import models, forms
from .forms import PetCreateForm, PetForm, AddServiceForm
from .models import Services, Customer, Pet, Service
from .serializers import ServicesSerializer

# Временное представление для API
class ServicesAPIView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

# Представление для начальной страницы (!) Рассчитываю, что там и должен быть список услуг (или нет?)
class ServicesList(ListView):
    model = Services
    ordering = '-created_time'
    template_name = 'home.html'
    context_object_name = 'home'
    #paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()


# вход для заказчика username = email
def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/profile/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.user_type == "заказчик":
                    login(request, user)
                    return redirect("/customer_profile")
                elif user1.user_type == "исполнитель":
                    login(request, user)
                    return redirect("/sitter_profile")
            else:
                thank = True
                return render(request, "sign/customer_login.html", {"thank": thank})
    return render(request, "sign/customer_login.html")


# создание записи питомца
class PetCreate(CreateView):
    form_class = PetCreateForm
    model = Pet
    template_name = 'pet_create.html'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.author = self.request.user.author
    #     post.save()
    #
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:customer_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


# редактирование питомца
class PetUpdate(LoginRequiredMixin, UpdateView):
    form_class = PetForm
    model = Pet
    template_name = 'pet_edit.html'

    def get_success_url(self):
        return reverse('user_app:customer_profile', kwargs={'username': self.request.user.username})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'pet_id': post.pk}
        # if post.host.user != self.request.user:
        #     return render(self.request, template_name='post_lock.html', context=context)
        return super(PetUpdate, self).dispatch(request, *args, **kwargs)


# удаление питомца
class PetDelete(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pet_delete.html'

    def get_success_url(self):
        return reverse('user_app:customer_profile', kwargs={'username': self.request.user.username})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'pet_id': post.pk}
        # if post.host.user != self.request.user:
        #     return render(self.request, template_name='post_lock.html', context=context)
        return super(PetDelete, self).dispatch(request, *args, **kwargs)


# добавление услуги
class AddService(CreateView):
    form_class = AddServiceForm
    model = Service
    template_name = 'add_service.html'

    def get_success_url(self):
        return reverse('user_app:sitter_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.sitter = self.request.user
        return super().form_valid(form)

