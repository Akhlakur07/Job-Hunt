from django.db import models

class user(models.Model):
    USER_TYPE = [
        ('job_seeker', 'Job Seeker'),
        ('company', 'Company')
    ]
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="templates", blank=True)

class job_seeker(models.Model):
    j_username = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True, related_name="job_hunter")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=30)
    gender = models.CharField(max_length=6)

class skills(models.Model):
    job_hunter = models.ForeignKey(job_seeker, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=50)
    experience = models.IntegerField()

class company(models.Model):
    c_username = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True, related_name="company")
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    establishment_year = models.DateField()

class jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    c_username = models.ForeignKey(company, on_delete=models.CASCADE, related_name="job_posted")
    req_skill = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    limit = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.CharField(max_length=400)
    req_experience = models.IntegerField()
    deadline = models.DateField()

class apply(models.Model):
    job_id = models.ForeignKey(jobs, on_delete=models.CASCADE, related_name="applied_jobs")
    j_username = models.ForeignKey(job_seeker, on_delete=models.CASCADE, related_name="applied_jobs")
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    cv = models.TextField()