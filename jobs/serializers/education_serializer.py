from rest_framework import serializers
from jobs.models.education import Education

class EducationSerializer(serializers.ModelSerializer):
    """Serializer for Education model with additional computed fields"""
    
    duration_months = serializers.SerializerMethodField()
    degree_display = serializers.CharField(source='get_degree_display', read_only=True)
    
    class Meta:
        model = Education
        fields = [
            'id',
            'user',
            'institution',
            'degree',
            'degree_display',
            'field_of_study',
            'start_date',
            'end_date',
            'is_current',
            'grade',
            'description',
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
    
    def validate(self, data):
        """Custom validation for education dates"""
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date must be after start date")
        
        if data.get('is_current') and data.get('end_date'):
            raise serializers.ValidationError("Cannot have end date if education is current")
        
        return data

class EducationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating education entries"""
    
    class Meta:
        model = Education
        fields = [
            'institution',
            'degree',
            'field_of_study',
            'start_date',
            'end_date',
            'is_current',
            'grade',
            'description'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
