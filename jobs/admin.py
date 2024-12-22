from django.contrib import admin
from jobs.models import *
# Register your models here.

admin.site.register(user)
admin.site.register(job_seeker)
admin.site.register(skills)
admin.site.register(company)
admin.site.register(jobs)
admin.site.register(apply)
