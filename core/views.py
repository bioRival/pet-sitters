from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse, Http404
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from rest_framework import generics

from . import models, forms
from .forms import PetCreateForm, PetForm, AddServiceForm
from .models import Services, Customer, Pet, Service
from .serializers import ServicesSerializer
import json
from django.core import serializers
import random
from datetime import date

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


# удаление услуги
class ServiceDelete(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service_delete.html'

    def get_success_url(self):
        return reverse('user_app:sitter_profile', kwargs={'username': self.request.user.username})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'service_id': post.pk}
        # if post.host.user != self.request.user:
        #     return render(self.request, template_name='post_lock.html', context=context)
        return super(ServiceDelete, self).dispatch(request, *args, **kwargs)


class SittersList(ListView):
    model = Customer
    template_name = 'sitters.html'
    context_object_name = 'sitters'


# публичный профиль ситтера
class SitterCardView(TemplateView):
    template_name = 'sitter_card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, id=self.kwargs.get('id'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['sitter_profile'] = user
        context['sitter_services'] = Service.objects.filter(sitter=user)
        context['title'] = f'Профиль пользователя {user}'
        return context


# view для каталога
class SearchSitters(View):
    model = Customer
    template_name = 'search.html'
    context_object_name = 'search'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context

    def get(self, request):
        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     number = 10
        #     return JsonResponse({'number': number})
        
        return render(request, 'search.html')
   
    def post(self, request):
        data = json.loads(request.body)

        # Значения полученные в POST запросе
        # Переменная  ||  Примеры значений
        # id_list           34, 35, 36          Лист id которые найдены на карте
        # pet_dog           True / False
        # pet_сat           True / False
        # date_start        '2024-06-14'
        # date_end          '2024-06-15'
        # service           'walk' / 'boarding' / 'daycare'
        # address           'Москва, Щукинская улица'
        # weight            'small' / 'medium' / 'large' / 'xlarge'
        #
        # Если значение не указано - None

        # Получение параметров фильтра
        id_list = data.get('idList', None)
        if id_list: 
            id_list = id_list.split(',')
            id_list = [int(num.strip()) for num in id_list]
        else:
            id_list = []
        pet_dog = bool(data.get('pet-dog', None))
        pet_cat = bool(data.get('pet-cat', None))
        date_start = data.get('date-start', None) or None
        date_end = data.get('date-end', None) or None
        service = data.get('service', None)
        address = data.get('address', None) or None
        weight = data.get('weight', None)

        print(f" \
              id_list: {list(id_list)}\n \
              pet_dog: {pet_dog}\n \
              pet_cat: {pet_cat}\n \
              date_start: {date_start}\n \
              date_end: {date_end}\n \
              service: {service}\n \
              address: {address}\n \
              weight: {weight} \
              ")

        #============== Поиск ситтеров ==============
        sitters = Customer.objects \
            .filter(user_type='исполнитель') \
            .filter(user_id__in=id_list)

        services = Service.objects \
            .filter(sitter_id__in=id_list)
        
        # Фильтр по виду питомца
        if pet_dog and not pet_cat:
            sitters = sitters.filter(cat_type__contains='dogsitter')
        elif pet_cat and not pet_dog:
            sitters = sitters.filter(cat_type__contains='catsitter')

        # Фильтр по виду услуги
        if service:
            if service == 'walk':
                sitters = sitters.filter(cat_type__contains='walk')
            elif service == 'boarding':
                sitters = sitters.filter(cat_type__contains='boarding')
            elif service == 'daycare':
                sitters = sitters.filter(cat_type__contains='daycare')
            

        tag_list = ['walk', 'boarding', 'daycare', 'dogsitter', 'catsitter']

        #============== Отправка найденных ситтеров ==============
        sitters_data = []
        for sitter in sitters:
            sitters_data.append({
                'id': sitter.user.pk,
                'name': sitter.user.first_name,
                'imageUrl': sitter.image.url,
                'age': get_age(sitter.dob),
                'orders': 26,
                'reviews': 11,
                'rating': sitter.rating,
                'quote': sitter.bio,
                'address': sitter.location,
                # 'price': sitter.service_sitter,
                # 'price': random.randint(500, 1000),
                'tags': sitter.cat_type,
                # 'tags': ['walk', 'dogsitter', 'catsitter'],
                # 'tags': random.choices(tag_list, k=random.randint(1, 3)),
                'coordinates': sitter.coordinates,
                'price': random.randint(500, 1000),
            })
        for service in services:
            sitters_data.append({
                'price': random.randint(500, 1000),
            })
        return JsonResponse(sitters_data, safe=False)





# Инфо на всех ситтеров в json формате
def get_all_sitters(request):
    # Поиск ситтеров
    sitters = Customer.objects \
        .filter(user_type = 'исполнитель')


    # Отправка найденных ситтеров
    sitters_data = []
    for sitter in sitters:
        sitters_data.append({
            'id': sitter.user.pk,
            'name': sitter.user.first_name,
            'coordinates': sitter.coordinates,
        })
    return JsonResponse(sitters_data, safe=False)







# Given a date of birth, returns age in full years
def get_age(dob):
    if dob is None:
        return None
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age
