# Generated by Django 5.0.3 on 2025-01-28 19:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_description', models.TextField(blank=True, null=True)),
                ('company_address', models.CharField(blank=True, max_length=255, null=True)),
                ('company_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('company_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('corporate_office_address', models.CharField(blank=True, max_length=255, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=20, null=True)),
                ('authorised_person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('authorised_person_position', models.CharField(blank=True, max_length=100, null=True)),
                ('authorised_person_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('authorised_person_email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('login_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('login_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('login_password', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
