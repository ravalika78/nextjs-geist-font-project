from rest_framework import serializers
from .models import Job, Company, UserProfile

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'location', 'logo', 'created_at']

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company', 'location', 
            'job_type', 'salary_min', 'salary_max', 'requirements', 
            'benefits', 'is_active', 'created_at', 'updated_at'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'skills', 'experience', 'education',
            'location', 'phone', 'linkedin_url', 'portfolio_url', 'profile_picture'
        ]
