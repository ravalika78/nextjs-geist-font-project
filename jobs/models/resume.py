from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Resume(models.Model):
    """Model to store user resumes with version control"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="Resume title or version name")
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="Upload PDF, DOC, or DOCX files only"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_primary = models.BooleanField(default=False, help_text="Mark as primary resume")
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size in bytes")
    file_type = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True, help_text="Description or notes about this resume")
    
    # Resume content analysis (can be populated by AI/parsing)
    parsed_skills = models.TextField(blank=True, help_text="Comma-separated skills extracted from resume")
    parsed_experience_years = models.PositiveIntegerField(null=True, blank=True)
    parsed_education_level = models.CharField(max_length=100, blank=True)
    
    # Usage tracking
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)
    applications_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-updated_at']
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Set file type and size
        if self.file:
            self.file_type = self.file.name.split('.')[-1].lower()
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        
        # Ensure only one primary resume per user
        if self.is_primary:
            Resume.objects.filter(user=self.user, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        
        super().save(*args, **kwargs)
    
    def get_file_size_display(self):
        """Return human-readable file size"""
        if not self.file_size:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def increment_download_count(self):
        """Increment download counter"""
        from django.utils import timezone
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded'])
