from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models.education import Education
from .models.experience import Experience
from .models.register import Register
from .models.resume import Resume
from .models.skills import Skill, Skills, SkillCategory, SkillEndorsement
from .models.userdetails import UserDetails

# Register models with admin interface

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['degree', 'is_current', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'institution', 'field_of_study']
    list_editable = ['is_current']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Institution Details', {
            'fields': ('institution', 'degree', 'field_of_study', 'grade')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'company', 'location', 'employment_type', 'start_date', 'end_date', 'is_current']
    list_filter = ['employment_type', 'is_current', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'job_title', 'company', 'location']
    list_editable = ['is_current']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Job Details', {
            'fields': ('job_title', 'company', 'location', 'employment_type')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Description', {
            'fields': ('description', 'skills_used', 'achievements')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'country', 'is_profile_complete', 'email_verified', 'phone_verified']
    list_filter = ['gender', 'country', 'is_profile_complete', 'email_verified', 'phone_verified']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city', 'country']
    readonly_fields = ['created_at', 'updated_at', 'is_profile_complete']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'bio')
        }),
        ('Social Links', {
            'fields': ('website', 'linkedin_url', 'github_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified', 'is_profile_complete'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'status', 'is_primary', 'file_type', 'download_count', 'applications_count', 'created_at']
    list_filter = ['status', 'is_primary', 'file_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'title', 'description']
    readonly_fields = ['file_size', 'file_type', 'download_count', 'applications_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('File Details', {
            'fields': ('title', 'file', 'status', 'is_primary', 'description')
        }),
        ('File Information', {
            'fields': ('file_size', 'file_type'),
            'classes': ('collapse',)
        }),
        ('Parsed Information', {
            'fields': ('parsed_skills', 'parsed_experience_years', 'parsed_education_level'),
            'classes': ('collapse',)
        }),
        ('Usage Statistics', {
            'fields': ('download_count', 'applications_count', 'last_downloaded'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = 'Number of Skills'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_trending', 'usage_count', 'created_at']
    list_filter = ['is_trending', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['usage_count', 'created_at']
    
    fieldsets = (
        ('Skill Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Status', {
            'fields': ('is_trending', 'usage_count')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'years_of_experience', 'verification_status', 'is_featured']
    list_filter = ['proficiency_level', 'verification_status', 'is_featured', 'created_at']
    search_fields = ['user__username', 'user__email', 'skill__name']
    readonly_fields = ['endorsement_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User & Skill', {
            'fields': ('user', 'skill')
        }),
        ('Proficiency', {
            'fields': ('proficiency_level', 'years_of_experience', 'verification_status')
        }),
        ('Details', {
            'fields': ('description', 'projects_used_in', 'certifications', 'last_used')
        }),
        ('Settings', {
            'fields': ('is_featured', 'endorsement_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(SkillEndorsement)
class SkillEndorsementAdmin(admin.ModelAdmin):
    list_display = ['user_skill', 'endorsed_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_skill__user__username', 'endorsed_by__username', 'user_skill__skill__name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Endorsement Details', {
            'fields': ('user_skill', 'endorsed_by', 'message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_job_title', 'current_company', 'years_of_experience', 'work_preference', 'profile_completion_percentage']
    list_filter = ['work_preference', 'employment_type_preference', 'availability', 'profile_visibility']
    search_fields = ['user__username', 'user__email', 'current_job_title', 'desired_job_title', 'industry']
    readonly_fields = ['profile_completion_percentage', 'job_search_activity_score', 'profile_views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Current Position', {
            'fields': ('current_job_title', 'current_company', 'industry', 'years_of_experience')
        }),
        ('Career Preferences', {
            'fields': ('desired_job_title', 'desired_industry', 'work_preference', 'employment_type_preference', 'availability')
        }),
        ('Salary Expectations', {
            'fields': ('expected_salary_min', 'expected_salary_max', 'salary_currency', 'salary_period', 'show_salary_expectations')
        }),
        ('Location & Relocation', {
            'fields': ('preferred_locations', 'willing_to_relocate')
        }),
        ('Profile Content', {
            'fields': ('summary', 'career_objectives', 'achievements', 'languages')
        }),
        ('Privacy Settings', {
            'fields': ('profile_visibility', 'allow_recruiter_contact')
        }),
        ('Notifications', {
            'fields': ('email_job_alerts', 'email_application_updates', 'email_marketing', 'sms_notifications')
        }),
        ('Statistics', {
            'fields': ('profile_completion_percentage', 'job_search_activity_score', 'profile_views_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
