from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='page_one'),

    path('buy/<int:route_id>/', views.buy_ticket, name='buy_ticket'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]
