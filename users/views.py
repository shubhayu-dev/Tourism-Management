# users/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# --- IMPORT BOTH of your models ---
from bookings.models import Package, Booking 

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request,'users/profile.html')

def package_list(request):
    packages = Package.objects.all()  # retrieve all rows
    
    # --- CRITICAL FIX ---
    # Your template needs the 'my_bookings' variable
    my_bookings = []
    if request.user.is_authenticated:
        my_bookings = Booking.objects.filter(user=request.user).order_by('-travel_date')

    # Pass both packages AND my_bookings to the template
    context = {
        'packages': packages,
        'my_bookings': my_bookings
    }
    return render(request, 'users/booking-page.html', context)


# --- NEW VIEW TO HANDLE BOOKING ---
@login_required
@require_POST
def create_booking_view(request):
    try:
        # 1. Load the JSON data sent from the JavaScript
        data = json.loads(request.body)
        
        # 2. Get data from the 'data' dictionary
        package_id = data.get('package_id')
        number_of_people = int(data.get('number_of_people', 1))
        
        # 3. Find the package in the database
        package = get_object_or_404(Package, package_id=package_id)
        
        # 4. Calculate the total price
        total_price = package.price * number_of_people
        
        # 5. Create the new booking object
        Booking.objects.create(
            user=request.user,
            package=package,
            number_of_people=number_of_people,
            total_amount=total_price,
            travel_date=data.get('travel_date'),
            phone=data.get('phone'),
            special_requests=data.get('special_requests', '')
            # The 'status' will use the default 'pending' from your model
        )
        
        # 6. Send a success response back to the JavaScript
        return JsonResponse({'success': True, 'message': 'Booking created!'})

    except Package.DoesNotExist:
        return JsonResponse({'error': 'Invalid package selected.'}, status=404)
    except Exception as e:
        # 7. Send an error response if anything goes wrong
        return JsonResponse({'error': str(e)}, status=400)
