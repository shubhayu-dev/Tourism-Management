import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Destination(models.Model):
    """Model representing travel destinations."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Destination Name")
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Country")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _("Destination")
        verbose_name_plural = _("Destinations")
    
    def __str__(self):
        return self.name


class Speciality(models.Model):
    """Model representing guide specialities/expertise areas."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Speciality Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _("Speciality")
        verbose_name_plural = _("Specialities")
    
    def __str__(self):
        return self.name


class Language(models.Model):
    """Model representing languages spoken by guides."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Language Name")
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        verbose_name=_("Language Code"),
        help_text=_("ISO 639-1 language code (e.g., 'en', 'es', 'fr')")
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
    
    def __str__(self):
        return self.name


class Guide(models.Model):
    """Model representing a tour guide with their details and specializations."""
    guide_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Guide ID"),
        help_text=_("Unique identifier for the guide")
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
        help_text=_("Full name of the guide")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description about the guide's experience and background")
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='guides',
        blank=True,
        verbose_name=_("Destinations"),
        help_text=_("Locations where the guide provides services")
    )
    specialities = models.ManyToManyField(
        Speciality,
        related_name='guides',
        blank=True,
        verbose_name=_("Specialities"),
        help_text=_("Guide's areas of expertise")
    )
    languages = models.ManyToManyField(
        Language,
        related_name='guides',
        blank=True,
        verbose_name=_("Languages"),
        help_text=_("Languages spoken by the guide")
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
        verbose_name=_("Rating"),
        help_text=_("Average rating out of 5.0")
    )
    rate_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Rate per Day"),
        help_text=_("Daily rate in your currency")
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name=_("Available"),
        help_text=_("Whether the guide is currently accepting bookings")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', 'name']
        verbose_name = _("Guide")
        verbose_name_plural = _("Guides")
    
    def __str__(self):
        return f"{self.name} ({self.guide_id})"
    
    def get_average_rating(self):
        """Calculate average rating from bookings"""
        from django.db.models import Avg
        avg = self.bookings.filter(
            status='completed',
            guide_rating__isnull=False
        ).aggregate(Avg('guide_rating'))
        return avg['guide_rating__avg']

