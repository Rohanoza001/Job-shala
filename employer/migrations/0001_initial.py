# Generated by Django 4.2.21 on 2025-07-25 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField()),
                ('resume', models.FileField(upload_to='application_resumes/')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('reviewing', 'Under Review'), ('shortlisted', 'Shortlisted'), ('interviewed', 'Interviewed'), ('hired', 'Hired'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='applied', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employer_notes', models.TextField(blank=True, null=True)),
                ('is_viewed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='employer_logos/')),
                ('designation', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('company_email', models.EmailField(max_length=254)),
                ('company_phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('gst_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employer.application')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='jobseeker_profiles/')),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company_name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('job_type', models.CharField(choices=[('full-time', 'Full Time'), ('part-time', 'Part Time'), ('contract', 'Contract'), ('internship', 'Internship'), ('freelance', 'Freelance')], max_length=20)),
                ('experience_level', models.CharField(choices=[('entry', 'Entry Level'), ('junior', 'Junior (1-3 years)'), ('mid', 'Mid Level (3-5 years)'), ('senior', 'Senior (5+ years)'), ('lead', 'Lead/Manager')], max_length=20)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_currency', models.CharField(default='INR', max_length=3)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('benefits', models.TextField(blank=True, null=True)),
                ('skills_required', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('views_count', models.IntegerField(default=0)),
                ('applications_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.employer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.job'),
        ),
        migrations.AddField(
            model_name='application',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.jobseeker'),
        ),
    ]
