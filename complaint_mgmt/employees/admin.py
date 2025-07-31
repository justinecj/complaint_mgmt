from django.contrib import admin
from .models import EmployeeProfile

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'phone', 'salary')
    search_fields = ('user__username', 'designation', 'phone')
