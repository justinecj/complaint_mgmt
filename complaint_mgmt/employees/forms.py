from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeProfile
from accounts.models import User

class EmployeeUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
        
    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if not name:
            raise forms.ValidationError("Name is required.")
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain only letters.")
        return name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'EMPLOYEE'
        if commit:
            user.save()
        return user


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['designation', 'phone', 'salary', 'personal_details']
        widgets = {
            'personal_details': forms.Textarea(attrs={'rows': 3}),
        }


class EmployeeUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name': 'Name',
        }
