from django.db import models
from django.contrib.auth.models import User

class SkillCategory(models.Model):
    """Categories for organizing skills"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class or icon name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    """Master list of skills"""
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='skills')
    description = models.TextField(blank=True)
    is_trending = models.BooleanField(default=False)
    usage_count = models.PositiveIntegerField(default=0, help_text="Number of users with this skill")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Skills(models.Model):
    """User skills with proficiency levels"""
    
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    VERIFICATION_STATUS_CHOICES = [
        ('unverified', 'Unverified'),
        ('self_assessed', 'Self Assessed'),
        ('certified', 'Certified'),
        ('endorsed', 'Endorsed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='unverified')
    
    # Additional details
    description = models.TextField(blank=True, help_text="Describe your experience with this skill")
    projects_used_in = models.TextField(blank=True, help_text="Projects where this skill was used")
    certifications = models.TextField(blank=True, help_text="Related certifications")
    
    # Endorsements
    endorsement_count = models.PositiveIntegerField(default=0)
    last_used = models.DateField(null=True, blank=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False, help_text="Show prominently on profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'skill']
        verbose_name = 'User Skill'
        verbose_name_plural = 'User Skills'
        ordering = ['-is_featured', '-proficiency_level', 'skill__name']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.proficiency_level})"
    
    def get_proficiency_percentage(self):
        """Convert proficiency level to percentage for UI display"""
        proficiency_map = {
            'beginner': 25,
            'intermediate': 50,
            'advanced': 75,
            'expert': 100,
        }
        return proficiency_map.get(self.proficiency_level, 0)

class SkillEndorsement(models.Model):
    """Skill endorsements from other users"""
    user_skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='endorsements')
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_endorsements')
    message = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_skill', 'endorsed_by']
        verbose_name = 'Skill Endorsement'
        verbose_name_plural = 'Skill Endorsements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.user_skill.user.username} for {self.user_skill.skill.name}"
