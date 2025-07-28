from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserDetails(models.Model):
    """Comprehensive user details and preferences"""
    
    AVAILABILITY_CHOICES = [
        ('immediately', 'Immediately'),
        ('2_weeks', 'Within 2 weeks'),
        ('1_month', 'Within 1 month'),
        ('2_months', 'Within 2 months'),
        ('3_months', 'Within 3 months'),
        ('not_looking', 'Not actively looking'),
    ]
    
    WORK_PREFERENCE_CHOICES = [
        ('remote', 'Remote only'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'On-site only'),
        ('flexible', 'Flexible'),
    ]
    
    EMPLOYMENT_TYPE_PREFERENCES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    
    # Professional Information
    current_job_title = models.CharField(max_length=200, blank=True)
    current_company = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    
    # Career Preferences
    desired_job_title = models.CharField(max_length=200, blank=True)
    desired_industry = models.CharField(max_length=100, blank=True)
    work_preference = models.CharField(max_length=20, choices=WORK_PREFERENCE_CHOICES, blank=True)
    employment_type_preference = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_PREFERENCES, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, blank=True)
    
    # Salary Expectations
    expected_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    salary_period = models.CharField(max_length=20, choices=[
        ('hourly', 'Per Hour'),
        ('monthly', 'Per Month'),
        ('yearly', 'Per Year'),
    ], default='yearly')
    
    # Location Preferences
    preferred_locations = models.TextField(blank=True, help_text="Comma-separated list of preferred work locations")
    willing_to_relocate = models.BooleanField(default=False)
    
    # Additional Information
    summary = models.TextField(blank=True, max_length=1000, help_text="Professional summary")
    career_objectives = models.TextField(blank=True, help_text="Career goals and objectives")
    achievements = models.TextField(blank=True, help_text="Key achievements and accomplishments")
    languages = models.TextField(blank=True, help_text="Languages spoken (comma-separated)")
    
    # Privacy Settings
    profile_visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('recruiters_only', 'Recruiters Only'),
    ], default='public')
    allow_recruiter_contact = models.BooleanField(default=True)
    show_salary_expectations = models.BooleanField(default=False)
    
    # Notification Preferences
    email_job_alerts = models.BooleanField(default=True)
    email_application_updates = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    
    # Profile Completion Tracking
    profile_completion_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    last_profile_update = models.DateTimeField(auto_now=True)
    
    # Activity Tracking
    last_login = models.DateTimeField(null=True, blank=True)
    job_search_activity_score = models.PositiveIntegerField(default=0)
    profile_views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'
    
    def __str__(self):
        return f"{self.user.username}'s Details"
    
    def calculate_profile_completion(self):
        """Calculate profile completion percentage"""
        fields_to_check = [
            self.current_job_title,
            self.years_of_experience,
            self.desired_job_title,
            self.work_preference,
            self.employment_type_preference,
            self.availability,
            self.summary,
            self.preferred_locations,
        ]
        
        completed_fields = sum(1 for field in fields_to_check if field)
        total_fields = len(fields_to_check)
        
        # Add points for related models
        if hasattr(self.user, 'user_skills') and self.user.user_skills.exists():
            completed_fields += 1
            total_fields += 1
        
        if hasattr(self.user, 'experiences') and self.user.experiences.exists():
            completed_fields += 1
            total_fields += 1
        
        if hasattr(self.user, 'education') and self.user.education.exists():
            completed_fields += 1
            total_fields += 1
        
        if hasattr(self.user, 'resumes') and self.user.resumes.exists():
            completed_fields += 1
            total_fields += 1
        
        percentage = int((completed_fields / total_fields) * 100) if total_fields > 0 else 0
        self.profile_completion_percentage = percentage
        self.save(update_fields=['profile_completion_percentage'])
        return percentage
    
    def get_experience_level(self):
        """Return experience level based on years of experience"""
        if not self.years_of_experience:
            return "Not specified"
        
        if self.years_of_experience < 2:
            return "Entry Level"
        elif self.years_of_experience < 5:
            return "Mid Level"
        elif self.years_of_experience < 10:
            return "Senior Level"
        else:
            return "Executive Level"
    
    def increment_profile_views(self):
        """Increment profile views counter"""
        self.profile_views_count += 1
        self.save(update_fields=['profile_views_count'])
