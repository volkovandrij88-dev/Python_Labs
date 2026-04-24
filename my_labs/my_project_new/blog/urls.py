from django.urls import path
from . import views  # Саме через крапку!

urlpatterns = [
    path('', views.home, name='page_one'),
    path('about/', views.about, name='page_two'),
]






