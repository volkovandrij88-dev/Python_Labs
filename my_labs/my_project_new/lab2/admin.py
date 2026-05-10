from django.contrib import admin
from .models import City, Route, Ticket # ЦЕЙ РЯДОК ОБОВ'ЯЗКОВИЙ

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'created_at', 'updated_at')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'route', 'created_at', 'updated_at')




