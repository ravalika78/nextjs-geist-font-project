from rest_framework import serializers
from jobs.models.resume import Resume

class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume model with computed fields"""
    
    file_size_display = serializers.SerializerMethodField()
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = [
            'id',
            'user',
            'title',
            'file',
            'status',
            'status_display',
            'is_primary',
            'file_size',
            'file_size_display',
            'file_type',
            'file_type_display',
            'description',
            'parsed_skills',
            'parsed_experience_years',
            'parsed_education_level',
            'download_count',
            'last_downloaded',
            'applications_count',
            'created_at',
            'updated_at',
            'download_url'
        ]
        read_only_fields = [
            'id', 'file_size', 'file_type', 'download_count', 
            'last_downloaded', 'applications_count', 'created_at', 'updated_at'
        ]
    
    def get_file_size_display(self, obj):
        """Return human-readable file size"""
        return obj.get_file_size_display()
    
    def get_download_url(self, obj):
        """Return download URL for the resume"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, value):
        """Validate file size and type"""
        max_file_size = 5 * 1024 * 1024  # 5MB
        
        if value.size > max_file_size:
            raise serializers.ValidationError("File size must be less than 5MB")
        
        allowed_extensions = ['pdf', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed")
        
        return value
    
    def validate(self, data):
        """Custom validation"""
        # Ensure only one primary resume per user
        if data.get('is_primary', False):
            user = self.context['request'].user
            existing_primary = Resume.objects.filter(user=user, is_primary=True)
            if self.instance:
                existing_primary = existing_primary.exclude(pk=self.instance.pk)
            
            if existing_primary.exists():
                raise serializers.ValidationError("You already have a primary resume")
        
        return data

class ResumeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Resume entries"""
    
    class Meta:
        model = Resume
        fields = [
            'title',
            'file',
            'status',
            'is_primary',
            'description',
            'parsed_skills',
            'parsed_experience_years',
            'parsed_education_level'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.save()  # This will set file_size and file_type
        return instance

class ResumeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Resume entries"""
    
    class Meta:
        model = Resume
        fields = [
            'title',
            'status',
            'is_primary',
            'description',
            'parsed_skills',
            'parsed_experience_years',
            'parsed_education_level'
        ]
