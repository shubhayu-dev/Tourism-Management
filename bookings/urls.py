from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/create/', views.create_booking, name='create_booking'),
]