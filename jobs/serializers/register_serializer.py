from rest_framework import serializers
from django.contrib.auth.models import User
from jobs.models.register import Register

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for Register model with user information"""
    
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Register
        fields = [
            'id',
            'user',
            'full_name',
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            'profile_picture',
            'profile_picture_url',
            'bio',
            'website',
            'linkedin_url',
            'github_url',
            'twitter_url',
            'is_profile_complete',
            'email_verified',
            'phone_verified',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_profile_complete']
    
    def get_full_name(self, obj):
        """Return user's full name"""
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    
    def get_profile_picture_url(self, obj):
        """Return profile picture URL or None"""
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        import re
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Invalid phone number format")
        return value
    
    def validate(self, data):
        """Custom validation"""
        # Ensure date of birth is not in the future
        if data.get('date_of_birth'):
            from datetime import date
            if data['date_of_birth'] > date.today():
                raise serializers.ValidationError("Date of birth cannot be in the future")
        return data

class RegisterCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Register entries"""
    
    class Meta:
        model = Register
        fields = [
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            'profile_picture',
            'bio',
            'website',
            'linkedin_url',
            'github_url',
            'twitter_url'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.check_profile_completeness()
        return instance
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.check_profile_completeness()
        return instance
