# Generated by Django 5.1.4 on 2024-12-31 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_job_seeker_j_username_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='cv',
            field=models.FileField(blank=True, upload_to='cv'),
        ),
        migrations.AlterUniqueTogether(
            name='apply',
            unique_together={('job_id', 'j_username')},
        ),
    ]