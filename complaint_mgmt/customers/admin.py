from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_details', 'address')
    search_fields = ('name', 'contact_details')
