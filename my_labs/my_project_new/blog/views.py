from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, TicketOrder, Newsletter, Rating


def home(request):
    search = request.GET.get("search", "")

    routes = Route.objects.all()

    if search:
        routes = routes.filter(to_city__icontains=search)

    return render(request, "blog/index.html", {
        "routes": routes,
        "search": search
    })


def buy_ticket(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    ratings = Rating.objects.filter(route=route)
    average_rating = 0

    if ratings.exists():
        total = sum(rating.value for rating in ratings)
        average_rating = round(total / ratings.count(), 1)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        count = request.POST.get("count")
        rating_value = request.POST.get("rating")

        if name and phone and count:
            TicketOrder.objects.create(
                route=route,
                name=name,
                phone=phone,
                count=count
            )

        if rating_value:
            Rating.objects.create(
                route=route,
                value=rating_value
            )

        return redirect("buy_ticket", route_id=route.id)

    return render(request, "blog/buy_ticket.html", {
        "route": route,
        "average_rating": average_rating,
        "ratings_count": ratings.count()
    })


def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            Newsletter.objects.get_or_create(email=email)

    return redirect("page_one")

def my_tickets(request):
    tickets = TicketOrder.objects.all().order_by("-created_at")

    return render(request, "blog/my_tickets.html", {
        "tickets": tickets
    })
