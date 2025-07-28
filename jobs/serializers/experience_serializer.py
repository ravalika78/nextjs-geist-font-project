from rest_framework import serializers
from jobs.models.experience import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience model with computed fields"""
    
    duration_months = serializers.SerializerMethodField()
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    skills_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = [
            'id',
            'user',
            'job_title',
            'company',
            'location',
            'employment_type',
            'employment_type_display',
            'start_date',
            'end_date',
            'is_current',
            'description',
            'skills_used',
            'skills_list',
            'achievements',
            'duration_months',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_duration_months(self, obj):
        """Calculate duration in months"""
        from datetime import date
        end = obj.end_date or date.today()
        return (end.year - obj.start_date.year) * 12 + (end.month - obj.start_date.month)
    
    def get_skills_list(self, obj):
        """Return skills as a list"""
        if obj.skills_used:
            return [skill.strip() for skill in obj.skills_used.split(',')]
        return []
    
    def validate(self, data):
        """Custom validation for experience dates"""
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date must be after start date")
        
        if data.get('is_current') and data.get('end_date'):
            raise serializers.ValidationError("Cannot have end date if experience is current")
        
        return data

class ExperienceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating experience entries"""
    
    class Meta:
        model = Experience
        fields = [
            'job_title',
            'company',
            'location',
            'employment_type',
            'start_date',
            'end_date',
            'is_current',
            'description',
            'skills_used',
            'achievements'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
