from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import json
from datetime import datetime, date

from .models import Package, Booking


def home(request):
    """Display packages and user bookings"""
    packages = Package.objects.filter(is_active=True).order_by('-created_at')
    
    my_bookings = []
    if request.user.is_authenticated:
        my_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'packages': packages,
        'my_bookings': my_bookings
    }
    return render(request, 'users/booking-page.html', context)


@login_required
@require_http_methods(["POST"])
def create_booking(request):
    """Create a new booking from JSON data"""
    try:
        data = json.loads(request.body)
        
        package_id = data.get('package_id')
        if not package_id:
            return JsonResponse({'success': False, 'error': 'Package ID is required.'}, status=400)
        
        package = get_object_or_404(Package, package_id=package_id, is_active=True)
        
        # Extract data
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        travel_date_str = data.get('travel_date', '').strip()
        number_of_people = data.get('number_of_people')
        special_requests = data.get('special_requests', '').strip()
        
        # Validate required fields
        if not all([full_name, email, phone, travel_date_str]):
            return JsonResponse({'success': False, 'error': 'All required fields must be filled.'}, status=400)
        
        # Validate number of people
        try:
            number_of_people = int(number_of_people)
            if number_of_people < 1:
                raise ValueError("Number must be at least 1")
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid number of people.'}, status=400)
        
        # Parse travel date
        try:
            travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            if travel_date <= date.today():
                return JsonResponse({'success': False, 'error': 'Travel date must be in the future.'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format.'}, status=400)
        
        # Calculate total
        total_amount = Decimal(str(package.price)) * number_of_people
        
        # Create booking
        booking = Booking.objects.create(
            package=package,
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            travel_date=travel_date,
            number_of_people=number_of_people,
            total_amount=total_amount,
            special_requests=special_requests,
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Booking created successfully!',
            'booking_id': str(booking.booking_id)
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        print(f"Booking error: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)