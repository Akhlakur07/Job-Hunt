from django.contrib import admin
from django.urls import path, include
from jobs import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('jobs.urls')),
]
