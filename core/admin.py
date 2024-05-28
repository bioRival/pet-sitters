from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Services)
admin.site.register(Author)
admin.site.register(Customer)

# Login Superuser: petsitadmin
# Password: qweasd
