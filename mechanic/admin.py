from django.contrib import admin
from . models import Mechanic
from . models import Customer
# Register your models here.
admin.site.register(Mechanic)
admin.site.register(Customer)


# admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    search_fields = ['user__username', 'message']
    list_filter = ['rating', 'created_at']

    from django.contrib import admin
from .models import MechanicProfile

admin.site.register(MechanicProfile)

from django.contrib import admin
from .models import CustomerProfile

admin.site.register(CustomerProfile)

from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'mechanic', 'date_requested', 'status', 'place', 'issue', 'vehicle_type', 'contact_number')
    search_fields = ('user__username', 'mechanic__user__username', 'place', 'issue', 'vehicle_type', 'contact_number')
    list_filter = ('status', 'vehicle_type')
    ordering = ('-date_requested',)
    readonly_fields = ('user', 'mechanic', 'date_requested')

admin.site.register(Request, RequestAdmin)

