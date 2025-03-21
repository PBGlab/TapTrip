from django.contrib import admin
from .models import Trip, TripDay


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'status')


@admin.register(TripDay)
class TripDayAdmin(admin.ModelAdmin):
    list_display = ('trip', 'date')
    
