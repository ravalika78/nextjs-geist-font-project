from django.db import models
from django.contrib.auth.models import User

class Experience(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('volunteer', 'Volunteer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    skills_used = models.TextField(blank=True, help_text="Comma-separated list of skills")
    achievements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"
    
    @property
    def duration_months(self):
        """Calculate duration in months"""
        from datetime import date
        end = self.end_date or date.today()
        return (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
