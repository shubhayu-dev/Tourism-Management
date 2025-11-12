# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # This path matches your package_list view and names it 'home'
    # This fixes: NoReverseMatch for 'home'
    path('book/', views.package_list, name='book'),
    
    # This path is for your new create_booking_view
    # This fixes the {% url 'create_booking' %} error
    path('create-booking/', views.create_booking_view, name='create_booking'),

    # This path is for your register_user view
    path('register/', views.register_user, name='register'),
    
    # This path is for your profile view
    path('profile/', views.profile, name='profile'),
    
    # --- Django's built-in auth views ---
    # Your register view redirects to 'login', so you need this
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Your template shows a 'Client Login' or 'My Bookings' button
    path('logout/', views.logout_view),
]