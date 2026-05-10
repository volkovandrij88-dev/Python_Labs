from django.contrib import admin
from .models import Route, TicketOrder, Newsletter, Rating

admin.site.register(Route)
admin.site.register(TicketOrder)
admin.site.register(Newsletter)
admin.site.register(Rating)
