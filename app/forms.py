from django import forms
from .models import *

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'