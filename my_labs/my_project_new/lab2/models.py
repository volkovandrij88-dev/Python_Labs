from django.db import models


# Таблиця 1: Міста
class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Місто")
    country = models.CharField(max_length=100, verbose_name="Країна")

    def __str__(self):
        return f"{self.name} ({self.country})"


# Таблиця 2: Маршрути (Об'єднує два міста)
class Route(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='starts', verbose_name="Звідки")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ends', verbose_name="Куди")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")

    # Вимога: поля створено/оновлено
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return f"{self.from_city.name} -> {self.to_city.name}"


# Таблиця 3: Квитки (Об'єднує пасажира і маршрут)
class Ticket(models.Model):
    passenger_name = models.CharField(max_length=150, verbose_name="ПІБ Пасажира")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Рейс")
    departure_date = models.DateTimeField(verbose_name="Дата та час виїзду")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return f"Квиток: {self.passenger_name} | {self.route}"