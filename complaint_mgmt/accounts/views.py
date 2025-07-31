from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, employee_required
from employees.models import EmployeeProfile
from customers.models import Customer
from products.models import Product
from complaints.models import Complaint
from django.utils.timezone import now  

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    
@never_cache
@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        # Fetch counts
        employee_count = EmployeeProfile.objects.count()
        customer_count = Customer.objects.count()
        product_count = Product.objects.count()
        complaint_count = Complaint.objects.count()

        context = {
            'employee_count': employee_count,
            'customer_count': customer_count,
            'product_count': product_count,
            'complaint_count': complaint_count,
            'now': now(),
        }
        return render(request, 'accounts/admin_dashboard.html', context)

    elif request.user.role == 'EMPLOYEE':

        assigned_count = Complaint.objects.filter(assigned_to=request.user).count()
        unassigned_count = Complaint.objects.filter(assigned_to__isnull=True).count()

        context = {
            'assigned_count': assigned_count,
            'unassigned_count': unassigned_count,
        }
        return render(request, 'accounts/employee_dashboard.html', context)

    else:
        messages.error(request, "Unauthorized role.")
        return redirect('login')
