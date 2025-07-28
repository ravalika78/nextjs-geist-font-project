from rest_framework import serializers
from jobs.models.skills import Skill, Skills, SkillCategory, SkillEndorsement

class SkillCategorySerializer(serializers.ModelSerializer):
    """Serializer for SkillCategory model"""
    
    skill_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'description', 'icon', 'skill_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_skill_count(self, obj):
        """Return count of skills in this category"""
        return obj.skills.count()

class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'description',
            'is_trending',
            'usage_count',
            'created_at'
        ]
        read_only_fields = ['id', 'usage_count', 'created_at']

class SkillsSerializer(serializers.ModelSerializer):
    """Serializer for User Skills model"""
    
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category.name', read_only=True)
    proficiency_display = serializers.CharField(source='get_proficiency_level_display', read_only=True)
    proficiency_percentage = serializers.SerializerMethodField()
    verification_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    
    class Meta:
        model = Skills
        fields = [
            'id',
            'user',
            'skill',
            'skill_name',
            'skill_category',
            'proficiency_level',
            'proficiency_display',
            'proficiency_percentage',
            'years_of_experience',
            'verification_status',
            'verification_display',
            'description',
            'projects_used_in',
            'certifications',
            'endorsement_count',
            'last_used',
            'is_featured',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'endorsement_count', 'created_at', 'updated_at']
    
    def get_proficiency_percentage(self, obj):
        """Return proficiency as percentage"""
        return obj.get_proficiency_percentage()
    
    def validate(self, data):
        """Custom validation"""
        if data.get('years_of_experience') and data.get('years_of_experience') > 50:
            raise serializers.ValidationError("Years of experience cannot exceed 50")
        
        return data

class SkillsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user skills"""
    
    class Meta:
        model = Skills
        fields = [
            'skill',
            'proficiency_level',
            'years_of_experience',
            'verification_status',
            'description',
            'projects_used_in',
            'certifications',
            'last_used',
            'is_featured'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class SkillEndorsementSerializer(serializers.ModelSerializer):
    """Serializer for Skill Endorsements"""
    
    endorsed_by_name = serializers.CharField(source='endorsed_by.get_full_name', read_only=True)
    skill_name = serializers.CharField(source='user_skill.skill.name', read_only=True)
    user_name = serializers.CharField(source='user_skill.user.get_full_name', read_only=True)
    
    class Meta:
        model = SkillEndorsement
        fields = [
            'id',
            'user_skill',
            'endorsed_by',
            'endorsed_by_name',
            'skill_name',
            'user_name',
            'message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """Custom validation"""
        # Prevent self-endorsement
        if data['endorsed_by'] == data['user_skill'].user:
            raise serializers.ValidationError("You cannot endorse your own skills")
        
        return data

class SkillEndorsementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating skill endorsements"""
    
    class Meta:
        model = SkillEndorsement
        fields = ['user_skill', 'message']
    
    def create(self, validated_data):
        validated_data['endorsed_by'] = self.context['request'].user
        return super().create(validated_data)
