# Generated by Django 5.1.4 on 2025-01-01 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_apply_cv_alter_apply_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='apply',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
