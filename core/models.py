from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title



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