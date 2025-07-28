from rest_framework import serializers
from jobs.models.userdetails import UserDetails

class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for UserDetails model with computed fields"""
    
    work_preference_display = serializers.CharField(source='get_work_preference_display', read_only=True)
    employment_type_preference_display = serializers.CharField(source='get_employment_type_preference_display', read_only=True)
    availability_display = serializers.CharField(source='get_availability_display', read_only=True)
    profile_visibility_display = serializers.CharField(source='get_profile_visibility_display', read_only=True)
    salary_period_display = serializers.CharField(source='get_salary_period_display', read_only=True)
    experience_level = serializers.SerializerMethodField()
    preferred_locations_list = serializers.SerializerMethodField()
    languages_list = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDetails
        fields = [
            'id',
            'user',
            'current_job_title',
            'current_company',
            'industry',
            'years_of_experience',
            'experience_level',
            'desired_job_title',
            'desired_industry',
            'work_preference',
            'work_preference_display',
            'employment_type_preference',
            'employment_type_preference_display',
            'availability',
            'availability_display',
            'expected_salary_min',
            'expected_salary_max',
            'salary_currency',
            'salary_period',
            'salary_period_display',
            'preferred_locations',
            'preferred_locations_list',
            'willing_to_relocate',
            'summary',
            'career_objectives',
            'achievements',
            'languages',
            'languages_list',
            'profile_visibility',
            'profile_visibility_display',
            'allow_recruiter_contact',
            'show_salary_expectations',
            'email_job_alerts',
            'email_application_updates',
            'email_marketing',
            'sms_notifications',
            'profile_completion_percentage',
            'last_profile_update',
            'last_login',
            'job_search_activity_score',
            'profile_views_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'profile_completion_percentage', 'last_profile_update',
            'job_search_activity_score', 'profile_views_count', 'created_at', 'updated_at'
        ]
    
    def get_experience_level(self, obj):
        """Return experience level based on years of experience"""
        return obj.get_experience_level()
    
    def get_preferred_locations_list(self, obj):
        """Return preferred locations as a list"""
        if obj.preferred_locations:
            return [location.strip() for location in obj.preferred_locations.split(',')]
        return []
    
    def get_languages_list(self, obj):
        """Return languages as a list"""
        if obj.languages:
            return [language.strip() for language in obj.languages.split(',')]
        return []
    
    def validate(self, data):
        """Custom validation"""
        # Validate salary range
        if data.get('expected_salary_min') and data.get('expected_salary_max'):
            if data['expected_salary_min'] > data['expected_salary_max']:
                raise serializers.ValidationError("Minimum salary cannot be greater than maximum salary")
        
        # Validate years of experience
        if data.get('years_of_experience') and data['years_of_experience'] > 50:
            raise serializers.ValidationError("Years of experience cannot exceed 50")
        
        return data

class UserDetailsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating UserDetails entries"""
    
    class Meta:
        model = UserDetails
        fields = [
            'current_job_title',
            'current_company',
            'industry',
            'years_of_experience',
            'desired_job_title',
            'desired_industry',
            'work_preference',
            'employment_type_preference',
            'availability',
            'expected_salary_min',
            'expected_salary_max',
            'salary_currency',
            'salary_period',
            'preferred_locations',
            'willing_to_relocate',
            'summary',
            'career_objectives',
            'achievements',
            'languages',
            'profile_visibility',
            'allow_recruiter_contact',
            'show_salary_expectations',
            'email_job_alerts',
            'email_application_updates',
            'email_marketing',
            'sms_notifications'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.calculate_profile_completion()
        return instance
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.calculate_profile_completion()
        return instance

class UserDetailsUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating UserDetails entries"""
    
    class Meta:
        model = UserDetails
        fields = [
            'current_job_title',
            'current_company',
            'industry',
            'years_of_experience',
            'desired_job_title',
            'desired_industry',
            'work_preference',
            'employment_type_preference',
            'availability',
            'expected_salary_min',
            'expected_salary_max',
            'salary_currency',
            'salary_period',
            'preferred_locations',
            'willing_to_relocate',
            'summary',
            'career_objectives',
            'achievements',
            'languages',
            'profile_visibility',
            'allow_recruiter_contact',
            'show_salary_expectations',
            'email_job_alerts',
            'email_application_updates',
            'email_marketing',
            'sms_notifications'
        ]
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.calculate_profile_completion()
        return instance
