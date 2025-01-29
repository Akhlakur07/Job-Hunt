# Job-Hunt
Job Hunt is a web-based platform developed using `Django`, `HTML`, and `CSS` to streamline the recruitment process by connecting job seekers with potential employers.

## Features

- Two types of user authentication:
    - Users can register as Job Seekers or Company.
- Job Seeker Portal:
    - Users can create profiles, browse job listings, and apply for suitable roles.
    - Job seekers can filter job postings based on salary, required experience, and skill.
- Employer Portal:
    - Employers can post job vacancies, including essential details like skills required, salary, experience, description, and application deadlines.
    - Employers can manage applications by accepting or declining them as needed.
- CRUD Functionality:
    - Both employers and job seekers have access to full Create, Read, Update, and Delete (CRUD) operations to manage profiles, jobs, and applications efficiently.

## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Django
- **Database**: SQlite

## Create database in the models.py file
```
from django.db import models

class user(models.Model):
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

```
Insert some dummy data
```
python manage.py shell
from jobs.models import *

# Create Users
user1 = user.objects.create(username="kakashi", password="password123", address="Hidden Leaf", bio="White fang")
user2 = user.objects.create(username="naruto", password="ramenlover99", address="Hidden Leaf", bio="Future Hokage")
user3 = user.objects.create(username="itachi", password="mangekyou123", address="Akatsuki Base", bio="Sharingan user")
user4 = user.objects.create(username="tsunade", password="medicNinja123", address="Hidden Leaf", bio="Medic Ninja")

# Create Job Seekers
job_seeker1 = job_seeker.objects.create(j_username=user1, first_name="Kakashi", last_name="Hatake", role="Ninja", gender="Male")
job_seeker2 = job_seeker.objects.create(j_username=user2, first_name="Naruto", last_name="Uzumaki", role="Hokage Trainee", gender="Male")
job_seeker3 = job_seeker.objects.create(j_username=user3, first_name="Itachi", last_name="Uchiha", role="Spy", gender="Male")

# Add Skills
skills.objects.create(job_hunter=job_seeker1, skill_name="Ninjutsu", experience=10)
skills.objects.create(job_hunter=job_seeker1, skill_name="Taijutsu", experience=8)
skills.objects.create(job_hunter=job_seeker2, skill_name="Shadow Clone", experience=7)
skills.objects.create(job_hunter=job_seeker3, skill_name="Genjutsu", experience=10)

# Create Companies
company1 = company.objects.create(c_username=user4, company_name="Leaf Hospital", company_type="Healthcare", establishment_year="2001-01-01")

# Post Jobs
job1 = jobs.objects.create(c_username=company1, req_skill="Healing", title="Medic Ninja", limit=5, salary=5000.000, description="Medical Support Specialist", req_experience=5, deadline="2024-12-31")
job2 = jobs.objects.create(c_username=company1, req_skill="Strategic Thinking", title="Strategist Ninja", limit=3, salary=6000.000, description="Battlefield Strategy Expert", req_experience=8, deadline="2024-12-31")

# Applications
apply.objects.create(job_id=job1, j_username=job_seeker1, accepted=False, rejected=False, cv="Highly experienced ninja specialized in combat and reconnaissance.")
apply.objects.create(job_id=job2, j_username=job_seeker2, accepted=True, rejected=False, cv="Aspiring Hokage with unmatched determination and drive.")
```


## Database EER Diagram

<img src="/doc/images/job_eer.png" alt="eer_diagram"/>