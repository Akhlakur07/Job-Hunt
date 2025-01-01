from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from .models import *
from random import sample
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.contrib import messages


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


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_instance = user.objects.get(username=username, password=password)
            request.session['username'] = user_instance.username  
            if user_instance.is_admin:
                return redirect('admin_dashboard')
            return redirect('home')
        except user.DoesNotExist:
            return render(request, 'jobs/login.html', {'error': "Invalid username or password"})
    return render(request, 'jobs/login.html')


def user_logout(request):
    logout(request)
    return redirect('login') 


def register_job_seeker(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        seeker_form = JobSeekerForm(request.POST)
        if user_form.is_valid() and seeker_form.is_valid():
            user_instance = user_form.save()
            job_seeker_instance = seeker_form.save(commit=False)
            job_seeker_instance.j_username = user_instance 
            job_seeker_instance.save()
            return redirect('login') 
    else:
        user_form = UserForm()
        seeker_form = JobSeekerForm()
    context = {'user_form': user_form, 'seeker_form': seeker_form}
    return render(request, 'jobs/register_job_seeker.html', context)


def register_company(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        company_form = CompanyForm(request.POST)
        if user_form.is_valid() and company_form.is_valid():
            user_instance = user_form.save()
            company_instance = company_form.save(commit=False)
            company_instance.c_username = user_instance 
            company_instance.save()
            return redirect('login') 
    else:
        user_form = UserForm()
        company_form = CompanyForm()
    return render(request, 'jobs/register_company.html', {'user_form': user_form, 'company_form': company_form})


def job_seeker_dashboard(request):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "job_seeker"):
        return redirect('login') 

    job_seeker_instance = user_instance.job_seeker
    applied_jobs = apply.objects.filter(j_username=job_seeker_instance)  
    skills_list = skills.objects.filter(job_hunter=job_seeker_instance)  

    if request.method == "POST":
        skill_name = request.POST.get('skill_name')
        experience = request.POST.get('experience')
        if skill_name and experience:
            skills.objects.create(job_hunter=job_seeker_instance, skill_name=skill_name, experience=experience)

    context = {
        'job_seeker': job_seeker_instance,
        'applied_jobs': applied_jobs,
        'skills': skills_list,
        'user': user_instance,
    }
    return render(request, 'jobs/seeker_dashboard.html', context)

def company_dashboard(request):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "company"):
        return redirect('login')  
    
    company_instance = user_instance.company
    posted_jobs = jobs.objects.filter(c_username=company_instance) 

    if request.method == "POST":
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.c_username = company_instance  
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

def view_jobs(request):
    search_query = request.GET.get('search', '') # Get search query ('search') from URL also default value is empty string ('')
    skill_filter = request.GET.get('skill', '')
    experience_filter = request.GET.get('experience', '')
    user_instance = user.objects.get(username=request.session['username'])
    if hasattr(user_instance, "job_seeker"):
        user_type = "Job Seeker" 
    else: 
        user_type = "Company"

    all_jobs = jobs.objects.all()
    
    if search_query:
        all_jobs = all_jobs.filter(title__icontains=search_query) #__icontains is case-insensitive
    if skill_filter:
        all_jobs = all_jobs.filter(req_skill__icontains=skill_filter)
    if experience_filter:
        all_jobs = all_jobs.filter(req_experience__lte=experience_filter)  # __lte is Less than or equal to

    context = {
        'jobs': all_jobs,
        'search_query': search_query,
        'skill_filter': skill_filter,
        'experience_filter': experience_filter,
        'user_type': user_type
    }
    return render(request, 'jobs/view_jobs.html', context)


def apply_for_job(request, job_id):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "job_seeker"):
        return redirect('login')  # Ensure only job seekers can apply

    job_seeker_instance = user_instance.job_seeker
    job_instance = get_object_or_404(jobs, job_id=job_id)

    # Check if the job seeker has already applied
    if apply.objects.filter(job_id=job_instance, j_username=job_seeker_instance).exists():
        return render(request, 'jobs/job_application_error.html', {
            'error': "You have already applied for this job."
        })

    # Check skill and experience requirements
    seeker_skills = skills.objects.filter(job_hunter=job_seeker_instance)
    skill_names = [skill.skill_name.lower() for skill in seeker_skills]
    max_experience = seeker_skills.aggregate(max_experience=Max('experience'))['max_experience']

    if job_instance.req_skill.lower() not in skill_names or job_instance.req_experience > (max_experience or 0):
        return render(request, 'jobs/job_application_error.html', {
            'error': "You do not meet the skill or experience requirements for this job."
        })

    # Handle CV upload and application creation
    if request.method == "POST":
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_id = job_instance
            application.j_username = job_seeker_instance
            application.save()
            return redirect('view_jobs')
    else:
        form = ApplyForm()

    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job_instance})



def view_applications(request):
    user_instance = user.objects.get(username=request.session['username'])
    # Ensure the user is a company
    if not hasattr(user_instance, 'company'):
        return redirect('login')

    # Fetch jobs posted by this company
    company = user_instance.company
    company_jobs = jobs.objects.filter(c_username=company)

    # Fetch applications for these jobs
    applications = apply.objects.filter(job_id__in=company_jobs).select_related('j_username', 'job_id')

    context = {
        'applications': applications,
    }
    return render(request, 'jobs/view_applications.html', context)


def manage_application(request, application_id, action):
    user_instance = user.objects.get(username=request.session['username'])
    if not hasattr(user_instance, "company"):
        return redirect('login')  # Ensure only companies can access

    application = get_object_or_404(apply, id=application_id)
    if action == "accept":
        application.accepted = True
        application.rejected = False
        messages.success(request, f"Congratulations! Your application for the job '{application.job_id.title}' has been accepted.")
    elif action == "reject":
        application.accepted = False
        application.rejected = True
        messages.error(request, f"Unfortunately, your application for the job '{application.job_id.title}' has been rejected.")
    application.save()
    return redirect('view_applications')




def admin_dashboard(request):
    user_instance = user.objects.get(username=request.session['username'])
    if user_instance.is_admin == False:
        return redirect('login')

    users = user.objects.all()
    applications = apply.objects.all()
    job_posts = jobs.objects.all()
    skills_list = skills.objects.all()
    return render(request, 'jobs/admin_dashboard.html', {
        'users': users,
        'applications': applications,
        'job_posts': job_posts,
        'skills': skills_list
    })

def delete_user(request, user_id):
    user_instance = get_object_or_404(user, pk=user_id)
    user_instance.delete()
    return redirect('admin_dashboard')

def approve_application(request, application_id, action):
    application = get_object_or_404(apply)
    if action == "accept":
        application.accepted = True
        application.rejected = False
    elif action == "reject":
        application.rejected = True
        application.accepted = False
    elif action == "pending":
        application.rejected = False
        application.accepted = False
    application.save()
    return redirect('admin_dashboard')

def delete_skill_a(request, skill_id):
    skill_instance = get_object_or_404(skills, pk=skill_id)
    skill_instance.delete()
    return redirect('admin_dashboard')

def delete_job_a(request, job_id):
    job_instance = get_object_or_404(jobs, pk=job_id)
    job_instance.delete()
    return redirect('admin_dashboard')

def delete_application_a(request, application_id):
    application_instance = get_object_or_404(apply, pk=application_id)
    application_instance.delete()
    return redirect('admin_dashboard')