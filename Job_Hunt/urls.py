from django.contrib import admin
from django.urls import path
from jobs import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/job_seeker/', views.register_job_seeker, name='register_job_seeker'),
    path('register/company/', views.register_company, name='register_company'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
