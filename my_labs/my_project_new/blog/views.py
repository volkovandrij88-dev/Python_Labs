from django.shortcuts import render

def home(request):

    routes = [
        {"from_city": "Київ", "to_city": "Варшава", "price": 1500, "image": "warsaw.jpg"},
        {"from_city": "Київ", "to_city": "Мінськ", "price": 650, "image": "minsk.jpg"},
        {"from_city": "Київ", "to_city": "Берлін", "price": 7500, "image": "berlin.jpg"},
        {"from_city": "Київ", "to_city": "Вільнюс", "price": 1700, "image": "vilnius.jpg"},
        {"from_city": "Київ", "to_city": "Рига", "price": 2000, "image": "riga.jpg"},
        {"from_city": "Київ", "to_city": "Таллінн", "price": 2500, "image": "tallinn.jpg"},
        {"from_city": "Київ", "to_city": "Гельсінкі", "price": 15000, "image": "helsinki.jpg"},
        {"from_city": "Київ", "to_city": "Стокгольм", "price": 18000, "image": "stockholm.jpg"},
        {"from_city": "Київ", "to_city": "Копенгаген", "price": 24800, "image": "copenhagen.jpg"},
    ]

    return render(request, "blog/index.html", {"routes": routes})
