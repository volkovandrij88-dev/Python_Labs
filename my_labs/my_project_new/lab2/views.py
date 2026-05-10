from django.shortcuts import render
from .models import City, Route


def index(request):
    # Беремо всі дані з бази
    cities = City.objects.all()
    routes = Route.objects.all()

    # Передаємо їх у шаблон
    return render(request, 'index.html', {
        'cities': cities,
        'routes': routes
    })

