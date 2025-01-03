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
    path('admin-c/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-c/delete_user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('admin-c/manage_application/<int:application_id>/<str:action>/', views.approve_application, name='approve_application'),
    path('admin-c/delete_skill/<int:skill_id>/', views.delete_skill_a, name='delete_skill_a'),
    path('admin-c/delete_job/<int:job_id>/', views.delete_job_a, name='delete_job_a'),
    path('admin-c/delete_application/<int:application_id>/', views.delete_application_a, name='delete_application_a'),
]
