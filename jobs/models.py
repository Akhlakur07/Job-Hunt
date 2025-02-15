from django.db import models

class user(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False) 
    address = models.CharField(max_length=300, null=True, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.username

class job_seeker(models.Model):
    j_username = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True, related_name="job_seeker")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=30)
    gender = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class skills(models.Model):
    job_hunter = models.ForeignKey(job_seeker, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=50)
    experience = models.IntegerField()

class company(models.Model):
    c_username = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True, related_name="company")
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    establishment_year = models.DateField()

    def __str__(self):
        return self.company_name


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
    cv = models.FileField(upload_to="cv", blank=True)