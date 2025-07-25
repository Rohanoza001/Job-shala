from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='jobseeker_profiles/', null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey('employer.Job', on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='application_resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employer_notes = models.TextField(blank=True, null=True)
    is_viewed = models.BooleanField(default=False)
    decision_made = models.BooleanField(default=False)  # Track if final decision has been made
    decision_date = models.DateTimeField(null=True, blank=True)  # When decision was made

    def __str__(self):
        return f"{self.job_seeker.user.get_full_name()} - {self.job.title}"

    def can_change_status(self):
        """Check if the status can still be changed"""
        # Can change if no final decision has been made
        return not self.decision_made

    def is_final_decision(self, status):
        """Check if the given status is a final decision"""
        return status in ['shortlisted', 'hired', 'rejected']

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'job_seeker']  # Prevent duplicate applications
