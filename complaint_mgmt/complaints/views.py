from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, ComplaintUpdate, COMPLAINT_STATUS
from .forms import ComplaintForm, ComplaintRemarkForm, ComplaintStatusUpdateForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, employee_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages

@login_required
@admin_required
def register_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/register.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

# @never_cache
# @login_required
# @admin_required
# def complaint_list(request):
#     complaints = Complaint.objects.select_related('customer', 'product', 'assigned_to').order_by('-created_at')
#     return render(request, 'complaints/complaint_list.html', {'complaints': complaints})
@never_cache
@login_required
@employee_required
def assigned_complaints(request):
    complaints = Complaint.objects.filter(assigned_to=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    return render(request, 'complaints/assigned_complaints.html', {
        'complaints': complaints
    })
    
@never_cache
@login_required
@employee_required
def unassigned_complaints(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        try:
            complaint = Complaint.objects.get(pk=complaint_id, assigned_to__isnull=True)
            complaint.assigned_to = request.user
            complaint.save()
            messages.success(request, f"Complaint #{complaint_id} assigned to you.")
        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found or already assigned.")

        return redirect('unassigned_complaints')  # reload page

    complaints = Complaint.objects.filter(assigned_to__isnull=True)
    return render(request, 'complaints/unassigned_complaints.html', {'complaints': complaints})

@never_cache
@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, assigned_to=request.user)
    remarks = complaint.updates.all().order_by('-timestamp')

    if request.method == 'POST':
        remark_form = ComplaintRemarkForm(request.POST)
        status_form = ComplaintStatusUpdateForm(request.POST, instance=complaint)

        if remark_form.is_valid() and status_form.is_valid():
            # Save remark
            remark = remark_form.save(commit=False)
            remark.complaint = complaint
            remark.updated_by = request.user  # Fixed field name
            remark.save()

            # Save status update
            status_form.save()

            messages.success(request, 'Updated successfully.')
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        remark_form = ComplaintRemarkForm()
        status_form = ComplaintStatusUpdateForm(instance=complaint)

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'remarks': remarks,
        'remark_form': remark_form,
        'status_form': status_form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })
    
@never_cache   
@login_required
@admin_required
def complaint_edit(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'complaints/edit_complaint.html', {
        'form': form,
        'title': 'Edit Complaint',
        'complaint': complaint,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })
@never_cache
@login_required
def complaint_readonly_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/complaint_readonly_detail.html', {
        'complaint': complaint,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY  
    })

@never_cache
@admin_required
@login_required
def complaint_list(request):
    selected_status = request.GET.get('status')
    
    complaints = Complaint.objects.all()
    if selected_status:
        complaints = complaints.filter(status=selected_status)

    context = {
        'complaints': complaints,
        'status_choices': COMPLAINT_STATUS,
        'selected_status': selected_status,
    }
    return render(request, 'complaints/complaint_list.html', context)

