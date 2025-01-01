from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/job-seeker/', views.register_job_seeker, name='register_job_seeker'),
    path('register/company/', views.register_company, name='register_company'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('seeker/dashboard/', views.job_seeker_dashboard, name='seeker_dashboard'),
    path('seeker/jobs/', views.view_jobs, name='view_jobs'),
    path('jobs/apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('company/applications/', views.view_applications, name='view_applications'),
    path('company/application/<int:application_id>/<str:action>/', views.manage_application, name='manage_application'),
]
