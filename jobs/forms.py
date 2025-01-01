from django import forms
from .models import user, job_seeker, company, jobs, apply

class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['username', 'password', 'address', 'bio', 'profile_pic']
        widgets = {
            'password': forms.PasswordInput(),  # Hide password input
        }

class JobSeekerForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

    class Meta:
        model = job_seeker
        fields = ['first_name', 'last_name', 'role', 'gender']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ['company_name', 'company_type', 'establishment_year']
    
    # Modify establishment_year field to be a DateField
    establishment_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select Year'})
    )

class JobForm(forms.ModelForm):
    class Meta:
        model = jobs
        fields = ['req_skill', 'title', 'limit', 'salary', 'description', 'req_experience', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplyForm(forms.ModelForm):
    class Meta:
        model = apply
        fields = ['cv']
        labels = {
            'cv': 'Upload CV',
        }
