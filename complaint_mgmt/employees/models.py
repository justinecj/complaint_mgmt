from django.db import models
from accounts.models import User

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    personal_details = models.TextField()
    
    def __str__(self):
        return self.user.username
