from django.contrib import admin
from .models import Category, Equipment, Rental, Payment

admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Rental)
admin.site.register(Payment)