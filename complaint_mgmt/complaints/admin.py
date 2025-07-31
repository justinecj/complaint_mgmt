from django.contrib import admin
from .models import Complaint, ComplaintUpdate

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'level', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'level', 'assigned_to')
    search_fields = ('customer__name', 'product__name', 'description')

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'updated_by', 'timestamp')
    search_fields = ('complaint__description', 'updated_by__username')
