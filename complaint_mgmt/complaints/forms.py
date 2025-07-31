from django import forms
from .models import Complaint, ComplaintUpdate

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'
        
class ComplaintRemarkForm(forms.ModelForm):
    class Meta:
        model = ComplaintUpdate
        fields = ['remark']

class ComplaintStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
