from django.contrib import admin
from .models import Sensor

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_factor', 'coc')
    search_fields = ('name',)