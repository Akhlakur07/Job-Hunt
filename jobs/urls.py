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
]
