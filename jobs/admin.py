from django.contrib import admin
from .models import Company, Job, JobApplication, UserProfile

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'website', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'created_at', 'company']
    search_fields = ['title', 'description', 'company__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'job__title', 'job__company__name']
    readonly_fields = ['applied_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone']
    search_fields = ['user__username', 'user__email', 'skills']
    list_filter = ['location']
