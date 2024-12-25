from django import forms
from .models import user, job_seeker, company

class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['username', 'password', 'address', 'bio', 'profile_pic']
        widgets = {
            'password': forms.PasswordInput(),  # Hide password input
        }

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = job_seeker
        fields = ['first_name', 'last_name', 'role', 'gender']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ['company_name', 'company_type', 'establishment_year']
