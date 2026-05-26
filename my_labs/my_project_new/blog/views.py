from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import Route, TicketOrder, Newsletter, Rating, PasswordResetCode

from reportlab.pdfgen import canvas
from io import BytesIO
import zipfile
import random


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
    if not request.user.is_authenticated:
        return render(request, "blog/need_register.html")

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
            count = int(count)

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

            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i in range(count):
                    pdf_buffer = BytesIO()
                    ticket_number = random.randint(100000, 999999)

                    p = canvas.Canvas(pdf_buffer)

                    p.setFont("Helvetica-Bold", 22)
                    p.drawString(100, 760, "TransportUA Ticket")

                    p.setFont("Helvetica", 14)
                    p.drawString(100, 710, f"Route: Kyiv - {route.to_city}")
                    p.drawString(100, 680, f"Ticket number: {ticket_number}")
                    p.drawString(100, 650, f"Passenger: {name}")
                    p.drawString(100, 620, f"Phone: {phone}")
                    p.drawString(100, 590, f"Price: {route.price} UAH")

                    p.showPage()
                    p.save()

                    pdf_buffer.seek(0)

                    filename = f"Kyiv-{route.to_city}-ticket-{ticket_number}.pdf"
                    zip_file.writestr(filename, pdf_buffer.read())

            zip_buffer.seek(0)

            response = HttpResponse(zip_buffer, content_type="application/zip")
            response["Content-Disposition"] = f'attachment; filename="Kyiv-{route.to_city}-tickets.zip"'

            return response

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


@login_required
def my_tickets(request):
    if request.user.is_superuser:
        tickets = TicketOrder.objects.all().order_by("-created_at")
    else:
        tickets = TicketOrder.objects.filter(user=request.user).order_by("-created_at")

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


@login_required
def profile(request):
    if request.user.is_staff:
        tickets = TicketOrder.objects.all().order_by("-created_at")
    else:
        tickets = TicketOrder.objects.filter(user=request.user).order_by("-created_at")

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
            generated_code = str(random.randint(100000, 999999))

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


