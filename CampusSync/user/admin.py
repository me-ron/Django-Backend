from django.contrib import admin
from .models import Address, Host, User
# Register your models here.
admin.site.register(Address)
admin.site.register(Host)
admin.site.register(User)