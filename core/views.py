from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from rest_framework import generics

from .forms import CreateProfileForm
from .models import Services, Customer
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


# регистрация заказчика username = email
def customer_signup(request):
    if request.method == "POST":
        username = request.POST['email']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # phone = request.POST['phone']
        # location = request.POST['location']
        # image = request.FILES['image']
        user_type = request.POST['user_type']

        if password1 != password2:
            messages.error(request, "Неправильный пароль.")
            return redirect('/customer_signup')

        user = User.objects.create_user(username=username,
                                        password=password1, email=email)
        customers = Customer.objects.create(user=user, user_type=user_type)

        # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
        #                                 password=password1, email=email)
        # customers = Customer.objects.create(user=user, phone=phone, location=location, image=image, user_type=user_type)
        user.save()
        customers.save()
        send_mail(
            subject='Регистрация пройдена успешно',
            message=f'Здравствуйте! Вы успешно зарегистрированы на сайте petsitters.ru.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        username = request.POST['email']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        login(request, user)

        return HttpResponseRedirect("/")
    return render(request, "sign/customer_signup.html")


class CustomerProfile(DetailView):
    model = Customer
    template_name = 'customer_profile.html'
    context_object_name = 'customer_profile'


class ShowProfilePageView(DetailView):
    model = Customer
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Customer.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Customer, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    form_class = CreateProfileForm
    model = Customer
    template_name = 'create_customer_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('services_list')


# редактируемый профиль
def customer_profile(request):
    if not request.user.is_authenticated:
        return redirect('/customer_login/')
    customer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        location = request.POST['location']

        customer.user.email = email
        customer.user.first_name = first_name
        customer.user.last_name = last_name
        customer.phone = phone
        customer.location = location
        customer.save()
        customer.user.save()

        # try:
        #     image = request.FILES['media']
        #     customer.image = image
        #     customer.save()
        # except:
        #     pass
        alert = True
        return render(request, "profile.html", {'alert': alert})
    return render(request, "profile.html", {'customer': customer})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/customer_login/')
