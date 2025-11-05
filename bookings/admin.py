from django.contrib import admin
from .models import Package, Booking


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'price', 'duration_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'destination', 'created_at']
    search_fields = ['name', 'destination', 'description']
    list_editable = ['is_active']
    readonly_fields = ['package_id', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('package_id', 'name', 'destination', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration_days')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'full_name', 'package', 'travel_date', 
                    'number_of_people', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'travel_date', 'created_at', 'package']
    search_fields = ['full_name', 'email', 'phone', 'booking_id']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'travel_date'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'package', 'status')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Travel Details', {
            'fields': ('travel_date', 'number_of_people', 'total_amount', 'special_requests')
        }),
        ('Guide Information', {
            'fields': ('guide', 'guide_amount', 'guide_rating', 'guide_review'),
            'classes': ('collapse',)  # Make this section collapsible
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'package', 'guide')