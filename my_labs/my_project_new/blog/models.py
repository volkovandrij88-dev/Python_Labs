from django.db import models


class Route(models.Model):
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.from_city} — {self.to_city}"


class TicketOrder(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.route.price * self.count

    def __str__(self):
        return f"{self.name} — {self.route}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Rating(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.route} — {self.value}"