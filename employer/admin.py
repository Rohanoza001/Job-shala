from django.contrib import admin
from .models import Employer, Job, Message

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'is_approved', 'is_verified', 'created_at']
    list_filter = ['is_approved', 'is_verified', 'created_at', 'country']
    search_fields = ['company_name', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_employers', 'reject_employers']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'designation', 'department')
        }),
        ('Contact Information', {
            'fields': ('phone', 'company_email', 'company_phone', 'company_website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'pincode')
        }),
        ('Business Information', {
            'fields': ('gst_number', 'company_logo')
        }),
        ('Approval Status', {
            'fields': ('is_approved', 'is_verified', 'approval_date', 'approval_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def approve_employers(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            is_approved=True,
            approval_date=timezone.now()
        )
        self.message_user(request, f'{updated} employer(s) have been approved.')
    approve_employers.short_description = "Approve selected employers"
    
    def reject_employers(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} employer(s) have been rejected.')
    reject_employers.short_description = "Reject selected employers"

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'company_name', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'experience_level', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'company_name', 'employer__company_name']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'applications_count']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'receiver__email', 'subject']
    readonly_fields = ['created_at']
