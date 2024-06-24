from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'brand', 'model', 'VIN', 'odometer', 'refresh_token')
    search_fields = ('manufacturer', 'brand', 'model', 'VIN')
    list_filter = ('manufacturer', 'brand', 'model')