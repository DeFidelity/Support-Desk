from django import forms 
from .models import SupportTicket

class CustomerRequestForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['summary','description','is_prioritized']