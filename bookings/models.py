import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

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
    image = models.ImageField(upload_to='packages/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Packages'
    
    def __str__(self):
        return self.name



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
        'Package',  # Assuming Package model exists
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
    
    # Guide (now as ForeignKey instead of CharField)
    guide = models.ForeignKey(
        'guide.Guide',  # ← Important: app_label.ModelName
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
        # Auto-calculate guide amount based on guide's rate
        if self.guide and not self.guide_amount:
            self.guide_amount = self.guide.rate_per_day
        super().save(*args, **kwargs)