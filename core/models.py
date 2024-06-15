from datetime import datetime
from multiselectfield import MultiSelectField

from PIL import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


from django.db.models import Sum
from django.utils import timezone

PACKAGES = [
    ('заказчик', 'Я - клиент'),
    ('исполнитель', 'Я - ситтер'),
]

CAT = [
    ('передержка', 'Передержка'),
    ('выгул', 'Выгул'),
    ('няня', 'Няня'),
]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(blank=True,
                           null=True,
                           verbose_name='Дата рождения')
    bio = models.TextField(max_length=70, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='images/profile/user_default.png',
                              upload_to="images/profile/%Y/%m/%d/")
    # last_visit = models.DateField(default=timezone.now, blank=True) # пока не поняла, как его запихнуть
    location = models.CharField(max_length=254, null=True, blank=True)
    area = models.CharField(max_length=254, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    user_type = models.CharField(choices=PACKAGES, max_length=20)
    cat_type = MultiSelectField(choices=CAT, max_choices=3, max_length=100, verbose_name='Профили работы')
    show_email = models.BooleanField(default=False,
                                     verbose_name='Показывать Email?')
    show_phone = models.BooleanField(default=False,
                                     verbose_name='Показывать телефон?')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user}'

    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def get_on_site(self):
        delta = datetime.now() - self.user.date_joined.replace(tzinfo=None)
        years = delta.days // 365
        if delta.days < 365:
            return 'менее года'
        else:
            on_site_string = ""
            if years == 1:
                on_site_string += f"{years} год, "
            elif 1 < years < 5:
                on_site_string += f"{years} года, "
            elif years >= 5:
                on_site_string += f"{years} лет"
            return on_site_string

    def get_age(self):
        if self.dob:
            today = datetime.today()
            age = today.year - self.dob.year

            if today.month < self.dob.month:
                age -= 1
            elif today.month == self.dob.month and today.day < self.dob.day:
                age -= 1

            return age

# Формирование рейтинга пользователя (!) Пока не знаю из чего он должен формироваться
#     def update_rating(self):
#         post_rating = Services.objects.filter(author=self).aggregate(
#             Sum('rating'))['rating__sum']
#         comment_rating = Comment.objects.filter(user=self.user).aggregate(
#             Sum('rating'))['rating__sum']
#         comment_rating_to_posts = Comment.objects.filter(
#             post__author__user=self.user).aggregate(Sum('rating'))[
#             'rating__sum']
#
#         self.rating = ((post_rating * 3) + comment_rating +
#                        comment_rating_to_posts)
#         self.save()
#
#     def __str__(self):
#         return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='service', verbose_name='Вид услуги')
    description = models.CharField(max_length=70, null=True, blank=True, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    sitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')


# Основная модель услуг (!) Не знаю какие категории должны быть, добавила временные
class Services(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=[
        ('котоняня', 'Котоняня'), ('собаконяня', 'Собаконяня')])
    created_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='ServicesCategory',
                                        related_name='ServicesCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} {self.text}'



class ServicesCategory(models.Model):
    postTrough = models.ForeignKey(Services, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)


# Откликами не занималась, просто модель
class Response(models.Model):
    text = models.TextField()
    datetime_response = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)

    def preview(self):
        if len(self.text) > 20:
            result = f'{self.text[:20]}...'
        else:
            result = self.text
        return result

    def get_absolute_url(self):
        return f'/response/{self.id}'

class Comment(models.Model):
    post = models.ForeignKey(Services, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Pet(models.Model):
    PETS = [
        ('собака', 'Собака'),
        ('кошка', 'Кошка')
    ]

    WEIGHT = [
        ('1-5 кг', '1-5 кг'),
        ('6-10 кг', '6-10 кг'),
        ('11-20 кг', '11-20 кг'),
        ('21+ кг', '21+ кг')
    ]

    AGE = [
        ('до 1 года', 'до 1 года'),
        ('1 - 5 лет', '1 - 5 лет'),
        ('5 - 8 лет', '5 - 8 лет'),
        ('старше 8 лет', 'старше 8 лет')
    ]

    pet_type = models.CharField(max_length=6, choices=PETS, default='собака', verbose_name='Тип питомца')
    image = models.ImageField(null=True, blank=True, default='images/profile/pet_default.png',
                              upload_to="images/pets/%Y/%m/%d/", verbose_name='Фото')
    name = models.CharField(max_length=50, verbose_name='Имя питомца')
    breed = models.CharField(max_length=50, null=True, blank=True, verbose_name='Порода')
    age = models.CharField(max_length=25, choices=AGE, default='до 1 года', verbose_name='Возраст')
    extra_info = models.TextField(null=True, blank=True, verbose_name='Дополнительная информация')
    weight = models.CharField(max_length=25, choices=WEIGHT, default='1-5 кг', verbose_name='Вес')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pet', verbose_name='Хозяин')




