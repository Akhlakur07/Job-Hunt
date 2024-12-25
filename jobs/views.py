from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, JobSeekerForm, CompanyForm
from .models import *
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

# Registration for Job Seeker
def register_job_seeker(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        seeker_form = JobSeekerForm(request.POST)
        if user_form.is_valid() and seeker_form.is_valid():
            user_instance = user_form.save()
            job_seeker_instance = seeker_form.save(commit=False)
            job_seeker_instance.j_username = user_instance  # Link Job Seeker to User
            job_seeker_instance.save()
            return redirect('login')  # Redirect to login page
    else:
        user_form = UserForm()
        seeker_form = JobSeekerForm()
    return render(request, 'register_job_seeker.html', {'user_form': user_form, 'seeker_form': seeker_form})

# Registration for Company
def register_company(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        company_form = CompanyForm(request.POST)
        if user_form.is_valid() and company_form.is_valid():
            user_instance = user_form.save()
            company_instance = company_form.save(commit=False)
            company_instance.c_username = user_instance  # Link Company to User
            company_instance.save()
            return redirect('login')  # Redirect to login page
    else:
        user_form = UserForm()
        company_form = CompanyForm()
    return render(request, 'register_company.html', {'user_form': user_form, 'company_form': company_form})

# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_instance = user.objects.get(username=username, password=password)
            request.session['username'] = user_instance.username  # Store session
            return redirect('home')  # Redirect to dashboard or any home page
        except user.DoesNotExist:
            return render(request, 'login.html', {'error': "Invalid username or password"})
    return render(request, 'login.html')

@login_required
def home(request):
    # Pass any data you want to display on the home page
    user_type = "Job Seeker" if hasattr(request.user, 'job_hunter') else "Company"
    return render(request, 'home.html', {'user_type': user_type, 'user': request.user})