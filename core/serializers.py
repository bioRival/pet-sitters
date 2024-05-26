from rest_framework import serializers
from .models import Services


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('title', 'text', 'content_type', 'created_time', 'author')
                  #'image'
        # В планах добавление картинки в поле услуг

       # Нужно добавить методы POST и тд, у меня не хватило времени(
