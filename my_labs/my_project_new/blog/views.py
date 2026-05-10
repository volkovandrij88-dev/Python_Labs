from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, TicketOrder, Newsletter, Rating
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from random import randint
from django.contrib.auth.decorators import login_required

def home(request):
    search = request.GET.get("search", "")

    routes = Route.objects.all()

    if search:
        routes = routes.filter(to_city__icontains=search)

    return render(request, "blog/index.html", {
        "routes": routes,
        "search": search
    })

@login_required
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
                user=request.user,
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
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect("page_one")

    return render(request, "blog/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("page_one")

    return render(request, "blog/login.html")


def logout_user(request):
    logout(request)
    return redirect("page_one")


def profile(request):

    if request.user.is_staff:
        tickets = TicketOrder.objects.all().order_by("-created_at")
    else:
        tickets = TicketOrder.objects.filter(
            user=request.user
        ).order_by("-created_at")

    return render(request, "blog/profile.html", {
        "tickets": tickets
    })


def reset_password(request):
    message = ""

    if request.method == "POST":

        username = request.POST.get("username")
        code = request.POST.get("code")
        new_password = request.POST.get("new_password")

        user = User.objects.filter(username=username).first()

        if user and not code:

            generated_code = str(randint(100000, 999999))

            PasswordResetCode.objects.create(
                user=user,
                code=generated_code
            )

            send_mail(
                "Код відновлення пароля",
                f"Ваш код: {generated_code}",
                "transportua@gmail.com",
                [user.email],
                fail_silently=True,
            )

            message = "Код відправлено на email"

        elif user and code and new_password:

            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code
            ).last()

            if reset_code:
                user.set_password(new_password)
                user.save()

                message = "Пароль успішно змінено"

    return render(request, "blog/reset_password.html", {
        "message": message
    })

    @login_required
    def my_tickets(request):

        if request.user.is_superuser:
            tickets = TicketOrder.objects.all()
        else:
            tickets = TicketOrder.objects.filter(user=request.user)

        return render(request, 'blog/my_tickets.html', {
            'tickets': tickets
        })


