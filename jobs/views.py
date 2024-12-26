from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserForm, JobSeekerForm, CompanyForm
from .models import *

# Home View
# @login_required(login_url='login')  # Redirect to login if not logged in
def home(request):
    user_instance = user.objects.get(username=request.session['username'])
    if hasattr(user_instance, "job_seeker"):
        return render(request, 'jobs/home.html', {'user': user_instance.job_seeker.first_name, 'user_type': "Job Seeker"})
    elif hasattr(user_instance, "company"):
        return render(request, 'jobs/home.html', {'user': user_instance.company.company_name, 'user_type': "Company"})

# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_instance = user.objects.get(username=username, password=password)
            request.session['username'] = user_instance.username  # store session
            return redirect('home')
        except user.DoesNotExist:
            return render(request, 'jobs/login.html', {'error': "Invalid username or password"})
    return render(request, 'jobs/login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login') 

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
            return redirect('login') 
    else:
        user_form = UserForm()
        seeker_form = JobSeekerForm()
    return render(request, 'jobs/register_job_seeker.html', {'user_form': user_form, 'seeker_form': seeker_form})

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
            return redirect('login') 
    else:
        user_form = UserForm()
        company_form = CompanyForm()
    return render(request, 'jobs/register_company.html', {'user_form': user_form, 'company_form': company_form})
