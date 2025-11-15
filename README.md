# Tourism and Package Management System

## 📖 Table of Contents

  * [📜 Abstract]
  * [✨ Key Features]
  * [🛠️ Tech Stack]
  * [🚀 Project Setup]
  * [🧪 Populating the Database (Optional)]
  * [🗃️ Database Schema]
  * [🖥️ Application Pages]
  * [📚 References]

-----

## 📜 Abstract

This project implements a web-based **Tourism and Package Management system**, built with Django. It provides packaged-travel management and booking functionality, user authentication, and administrative interfaces for managing packages, guides, and bookings. The application is designed to simplify package creation, customer bookings, and basic operational workflows for a small travel agency. Emphasis is on modularity, maintainability, and ease of testing.

-----

## ✨ Key Features

  * **Package Management:** Full **CRUD** (Create, Read, Update, Delete) operations for travel packages.
  * **Guide Management:** Administrators can add, edit, and manage tour guides.
  * **Customer Bookings:** Users can browse available packages, search, and submit bookings.
  * **Admin Dashboard:** An admin interface (using Django Admin) allows staff to manage and approve bookings, update package details, and oversee operations.

-----

## 🛠️ Tech Stack

  * **Backend:** Django (Python)
  * **Frontend:** Django Templates (Server-Side Rendering)
  * **Database:** Django ORM with MySQL
  * **Admin:** Built-in Django Admin Interface

-----

## 🚀 Project Setup

### 1\. Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2\. Create and Activate a Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate it:
# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3\. Install Dependencies

Install all required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

*(Alternatively, if `requirements.txt` is missing, install core packages manually):*

```bash
pip install django mysqlclient python-dotenv
```

### 4\. Create a `.env` File

Create a `.env` file in the project root directory. This file stores your secret keys and database configuration.

**Example `.env`:**

```ini
SECRET_KEY=django-insecure-xxxxxx
DEBUG=True

DB_NAME=tourism_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```

### 5\. Configure the Database

Open your MySQL client and create the database specified in your `.env` file.

```sql
CREATE DATABASE tourism_db;
```

### 6\. Apply Migrations

Run Django's migrate commands to create the database tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7\. Run the Server

Start the development server.

```bash
python manage.py runserver
```

Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

-----

## 🧪 Populating the Database (Optional)

You can add sample data for testing using the Django shell.

**1. Open the Django Shell:**

```bash
python manage.py shell
```

**2. Import Required Models:**

```python
from bookings.models import Package, Booking
from django.contrib.auth import get_user_model
User = get_user_model()
```

**3. Create or Fetch a User:**

```python
user = User.objects.filter(username="john_doe").first()

if not user:
    user = User.objects.create_user(
        username="john_doe",
        email="johndoe@example.com",
        password="secret"
    )

print("User ready:", user)
```

**4. Add Sample Packages:**

```python
p1 = Package.objects.create(
    name="Goa Beach Retreat",
    destination="Goa",
    description="Enjoy sun, sand, and sea with our exclusive Goa package.",
    duration_days=5,
    price=14999.99
)

p3 = Package.objects.create(
    name="China Exploration",
    destination="China",
    description="Soak in the rich culture, cuisines and monuments of China.",
    duration_days=10,
    price=30000.00
)

print("Added Packages:", Package.objects.all())
```

**5. Create a Sample Booking:**

```python
b1 = Booking.objects.create(
    package=p1,
    user=user,
    full_name="Ravi Sharma",
    email="ravi@example.com",
    phone="9876543210",
    travel_date="2025-11-15",
    number_of_people=2,
    total_amount=29999.98
)

print("Booking created:", b1)
```

**6. Exit the Shell:**

```python
exit()
```

-----

## 🗃️ Database Schema

The relational schema is designed in **3rd Normal Form (3NF)**.

### ER Diagram

### Relational Schema Design

[Image of the Relational Schema]

### Key Models

#### `Package` (from `bookings/models.py`)

```python
import uuid
from django.db import models

class Package(models.Model):
    """Tourism packages"""
    package_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    description = models.TextField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Packages'
    
    def __str__(self):
        return self.name
```

#### `Booking` (from `bookings/models.py`)

```python
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid

# Assumes 'guide.Guide' and 'Package' models exist
# from guide.models import Guide
# from .models import Package 

class Booking(models.Model):
    """Customer bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    package = models.ForeignKey(
        'Package',  # Assumes Package is in the same app or imported
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Customer details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Booking info
    travel_date = models.DateField()
    number_of_people = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    guide = models.ForeignKey(
        'guide.Guide', # Assumes Guide is in 'guide' app
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    guide_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Guide Fee"),
        help_text=_("Fee charged for the guide service")
    )
    guide_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
        verbose_name=_("Guide Rating"),
        help_text=_("Customer rating for the guide (0-5)")
    )
    guide_review = models.TextField(
        blank=True,
        verbose_name=_("Guide Review"),
        help_text=_("Customer review/feedback for the guide")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    special_requests = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.package.name}"
    
    def save(self, *args, **kwargs):
        # Assumes Guide model has 'rate_per_day' field
        if self.guide and not self.guide_amount:
            self.guide_amount = self.guide.rate_per_day
        super().save(*args, **kwargs)
```

-----

## 🖥️ Application Pages

  * **Public:**
      * Home / Packages List (`templates/bookings/list.html`)
      * Package Detail & Booking Form (`templates/bookings/detail.html`)
      * Login Page
      * Sign Up Page
  * **User (Authenticated):**
      * Booking Confirmation
      * Booking History
  * **Staff:**
      * Agent Dashboard
      * Django Admin Interface (for all CRUD operations)

-----

## 📚 References

  * [Django Documentation](https://docs.djangoproject.com/)
  * [dbdiagram.io](https://dbdiagram.io/) (Used for database schema design)
