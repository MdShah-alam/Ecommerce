from django.contrib import admin
from . import models
from django.contrib.auth.models import User

admin.site.register(models.Category)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Profile)


class ProfileInLine(admin.StackedInline):
    model = models.Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInLine]
    
# unregister old way
admin.site.unregister(models.User)

# re_register new way
admin.site.register(models.User , UserAdmin)
