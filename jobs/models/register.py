from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Register(models.Model):
    """Extended user registration model with additional profile information"""
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration_profile')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_profile_complete = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Registration'
        verbose_name_plural = 'User Registrations'
    
    def __str__(self):
        return f"{self.user.username}'s Registration Profile"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    def check_profile_completeness(self):
        """Check if profile is complete and update the flag"""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.phone_number,
            self.city,
            self.country,
        ]
        self.is_profile_complete = all(field for field in required_fields)
        self.save(update_fields=['is_profile_complete'])
        return self.is_profile_complete
