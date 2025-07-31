from django.db import models
from customers.models import Customer
from products.models import Product
from accounts.models import User

COMPLAINT_LEVELS = (
    ('L1', 'Level 1'),
    ('L2', 'Level 2'),
    ('L3', 'Level 3'),
)

COMPLAINT_STATUS = (
    ('Pending', 'Pending'),
    ('Closed', 'Closed'),
    ('Not Closed', 'Not Closed'),
)

class Complaint(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=COMPLAINT_LEVELS)
    description = models.TextField()
    location = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'EMPLOYEE'}
    )
    status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.pk} - {self.customer.name} ({self.status})"

class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    remark = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for Complaint #{self.complaint.pk} by {self.updated_by.username}"
