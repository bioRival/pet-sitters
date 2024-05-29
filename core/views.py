from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from rest_framework import generics
from .models import Services, BaseRegisterForm, Customer
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


# регистрационная вьюха
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


# вход для заказчика username = email
def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        image = request.FILES['image']
        user_type = request.POST['user_type']

        if password1 != password2:
            messages.error(request, "Неправильный пароль.")
            return redirect('/customer_signup')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password1, email=email)
        customers = Customer.objects.create(user=user, phone=phone, location=location, image=image, user_type=user_type)
        user.save()
        customers.save()
        return render(request, "sign/customer_login.html")
    return render(request, "sign/customer_signup.html")


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

        try:
            image = request.FILES['media']
            customer.image = image
            customer.save()
        except:
            pass
        alert = True
        return render(request, "customer_profile.html", {'alert': alert})
    return render(request, "customer_profile.html", {'customer': customer})
