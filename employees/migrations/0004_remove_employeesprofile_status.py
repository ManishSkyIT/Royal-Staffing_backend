# Generated by Django 5.0.3 on 2025-02-12 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_employeesprofile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeesprofile',
            name='status',
        ),
    ]
