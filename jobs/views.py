from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UserForm, JobSeekerForm, CompanyForm, JobForm
from .models import *
from django.db.models import Count
from random import sample

# Home View
def home(request):
    user_instance = user.objects.get(username=request.session['username'])
    
    # Fetch random 3 jobs
    all_jobs = jobs.objects.all()
    featured_jobs = sample(list(all_jobs), min(3, len(all_jobs)))

    if hasattr(user_instance, "job_seeker"):
        context = {
            'user': user_instance.job_seeker.first_name,
            'user_type': "Job Seeker",
            'featured_jobs': featured_jobs
        }
        return render(request, 'jobs/homes.html', context)
    elif hasattr(user_instance, "company"):
        context = {
            'user': user_instance.company.company_name,
            'user_type': "Company",
            'featured_jobs': featured_jobs
        }
        return render(request, 'jobs/homes.html', context)

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
    context = {'user_form': user_form, 'seeker_form': seeker_form}
    return render(request, 'jobs/register_job_seeker.html', context)

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


def company_dashboard(request):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "company"):
        return redirect('login')  # Redirect to login if user is not a company
    
    company_instance = user_instance.company
    posted_jobs = jobs.objects.filter(c_username=company_instance)  # Fetch jobs posted by the company

    if request.method == "POST":
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.c_username = company_instance  # Link job to the company
            job.save()
            return redirect('company_dashboard')
    else:
        job_form = JobForm()

    context = {
        'company': company_instance,
        'posted_jobs': posted_jobs,
        'user' : user_instance,
        'job_form': job_form
    }
    return render(request, 'jobs/company_dashboard.html', context)


def edit_job(request, job_id):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "company"):
        return redirect('login')

    company_instance = user_instance.company
    job_instance = jobs.objects.get(job_id=job_id, c_username=company_instance)

    if request.method == "POST":
        job_form = JobForm(request.POST, instance=job_instance)
        if job_form.is_valid():
            job_form.save()
            return redirect('company_dashboard')
    else:
        job_form = JobForm(instance=job_instance)

    context = {
        'job_form': job_form,
        'job': job_instance,
        'company': company_instance,
    }
    return render(request, 'jobs/edit_job.html', context)



def delete_job(request, job_id):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "company"):
        return redirect('login')

    company_instance = user_instance.company
    job_instance = jobs.objects.get(job_id=job_id, c_username=company_instance)

    if request.method == "POST":
        job_instance.delete()
        return redirect('company_dashboard')

    context = {
        'job': job_instance,
        'company': company_instance,
    }
    return render(request, 'jobs/delete_job.html', context)