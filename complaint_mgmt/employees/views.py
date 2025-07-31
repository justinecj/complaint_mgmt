from django.shortcuts import render, redirect, get_object_or_404
from .models import EmployeeProfile
# from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.views.decorators.cache import never_cache
from .forms import EmployeeUserCreationForm, EmployeeProfileForm, EmployeeUserEditForm

@never_cache
@login_required
@admin_required
def employee_list(request):
    employees = EmployeeProfile.objects.select_related('user').all()
    return render(request, 'employees/employee_list.html', {'employees': employees})
@never_cache
@login_required
@admin_required
def employee_create(request):
    if request.method == 'POST':
        user_form = EmployeeUserCreationForm(request.POST)
        profile_form = EmployeeProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('employee_list')
    else:
        user_form = EmployeeUserCreationForm()
        profile_form = EmployeeProfileForm()

    return render(request, 'employees/create_employee.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Add Employee',
    })

# @login_required
# @admin_required
# def employee_create(request):
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm()
#     return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})

@never_cache
@login_required
@admin_required
def employee_edit(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    user = profile.user

    if request.method == 'POST':
        user_form = EmployeeUserEditForm(request.POST, instance=user) 
        profile_form = EmployeeProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('employee_list')
    else:
        user_form = EmployeeUserEditForm(instance=user)
        profile_form = EmployeeProfileForm(instance=profile)

    return render(request, 'employees/edit_employee.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit Employee',
    })

@never_cache  
@login_required 
@admin_required
def employee_detail(request, pk):
    employee = get_object_or_404(EmployeeProfile.objects.select_related('user'), pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

