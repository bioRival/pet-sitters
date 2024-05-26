from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

# Формирование рейтинга пользователя (!) Пока не знаю из чего он должен формироваться
    def update_rating(self):
        post_rating = Services.objects.filter(author=self).aggregate(
            Sum('rating'))['rating__sum']
        comment_rating = Comment.objects.filter(user=self.user).aggregate(
            Sum('rating'))['rating__sum']
        comment_rating_to_posts = Comment.objects.filter(
            post__author__user=self.user).aggregate(Sum('rating'))[
            'rating__sum']

        self.rating = ((post_rating * 3) + comment_rating +
                       comment_rating_to_posts)
        self.save()

    def __str__(self):
        return self.user.username


# Я бы пользователя скорее в таком виде рассматривала, чтобы сразу роль была видна
PACKAGES = [
    ('заказчик', 'Заказчик'),
    ('Зооняня', 'Зооняня'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # image = models.ImageField(default='user_avatar.png', upload_to='...')
    last_visit = models.DateField(default=timezone.now, blank=True)
    location = models.CharField(max_length=254, null=True, blank=True)
    contact_phone = models.CharField(max_length=15)
    user_role = models.CharField(default="заказчик", choices=PACKAGES, max_length=20)


# А что у нас вообще в категориях будет? Сюда, по-хорошему, как раз услуги надо закидывать, типа Передержки, Груминга и т.д.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Основная модель услуг (!) Не знаю какие категории должны быть, добавила временные
class Services(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
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

#Откликами не занималась, просто модель
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