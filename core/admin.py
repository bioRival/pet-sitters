from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Services)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Pet)
admin.site.register(Service)
admin.site.register(ServiceCategory)

# Login Superuser: petsitadmin
# Password: qweasd
