from django import forms
from .models import Profile
class profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_picture','bio','dob']
        widgets={
            'dob':forms.DateInput(attrs={'type':'date'})
        }
