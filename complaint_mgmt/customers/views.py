from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required
@admin_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@never_cache
@login_required
@admin_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})

@never_cache
@login_required
@admin_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit Customer'})
