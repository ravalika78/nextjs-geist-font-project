from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models.education import Education
from .models.experience import Experience
from .models.register import Register
from .models.resume import Resume
from .models.skills import Skill, Skills, SkillCategory, SkillEndorsement
from .models.userdetails import UserDetails

from .serializers.education_serializer import EducationSerializer, EducationCreateSerializer
from .serializers.experience_serializer import ExperienceSerializer, ExperienceCreateSerializer
from .serializers.register_serializer import RegisterSerializer, RegisterCreateSerializer
from .serializers.resume_serializer import ResumeSerializer, ResumeCreateSerializer, ResumeUpdateSerializer
from .serializers.skills_serializer import (
    SkillSerializer, SkillsSerializer, SkillsCreateSerializer,
    SkillCategorySerializer, SkillEndorsementSerializer, SkillEndorsementCreateSerializer
)
from .serializers.userdetails_serializer import (
    UserDetailsSerializer, UserDetailsCreateSerializer, UserDetailsUpdateSerializer
)

class EducationViewSet(viewsets.ModelViewSet):
    """ViewSet for Education model"""
    
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['degree', 'is_current']
    search_fields = ['institution', 'field_of_study']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-end_date', '-start_date']
    
    def get_queryset(self):
        """Return education entries for the current user"""
        return Education.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return EducationCreateSerializer
        return EducationSerializer
    
    def perform_create(self, serializer):
        """Set user when creating education entry"""
        serializer.save(user=self.request.user)

class ExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for Experience model"""
    
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employment_type', 'is_current']
    search_fields = ['job_title', 'company', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-end_date', '-start_date']
    
    def get_queryset(self):
        """Return experience entries for the current user"""
        return Experience.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return ExperienceCreateSerializer
        return ExperienceSerializer
    
    def perform_create(self, serializer):
        """Set user when creating experience entry"""
        serializer.save(user=self.request.user)

class RegisterViewSet(viewsets.ModelViewSet):
    """ViewSet for Register model"""
    
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['gender', 'country', 'is_profile_complete']
    search_fields = ['city', 'state', 'country']
    
    def get_queryset(self):
        """Return registration profile for the current user"""
        return Register.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return RegisterCreateSerializer
        return RegisterSerializer
    
    def perform_create(self, serializer):
        """Set user when creating registration profile"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def check_completeness(self, request, pk=None):
        """Check and update profile completeness"""
        register = self.get_object()
        is_complete = register.check_profile_completeness()
        return Response({
            'is_complete': is_complete,
            'completion_percentage': 100 if is_complete else 0
        })

class ResumeViewSet(viewsets.ModelViewSet):
    """ViewSet for Resume model"""
    
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'is_primary', 'file_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'download_count']
    ordering = ['-is_primary', '-updated_at']
    
    def get_queryset(self):
        """Return resumes for the current user"""
        return Resume.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return ResumeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ResumeUpdateSerializer
        return ResumeSerializer
    
    def perform_create(self, serializer):
        """Set user when creating resume"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Track resume download"""
        resume = self.get_object()
        resume.increment_download_count()
        return Response({
            'download_url': resume.file.url,
            'download_count': resume.download_count
        })
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set resume as primary"""
        resume = self.get_object()
        # Remove primary status from other resumes
        Resume.objects.filter(user=request.user, is_primary=True).update(is_primary=False)
        # Set this resume as primary
        resume.is_primary = True
        resume.save()
        return Response({'message': 'Resume set as primary'})

class SkillCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for SkillCategory model (read-only)"""
    
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Skill model (read-only)"""
    
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_trending']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'usage_count', 'created_at']
    ordering = ['name']

class SkillsViewSet(viewsets.ModelViewSet):
    """ViewSet for User Skills model"""
    
    serializer_class = SkillsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['proficiency_level', 'verification_status', 'is_featured']
    search_fields = ['skill__name', 'description']
    ordering_fields = ['proficiency_level', 'years_of_experience', 'created_at']
    ordering = ['-is_featured', '-proficiency_level']
    
    def get_queryset(self):
        """Return skills for the current user"""
        return Skills.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return SkillsCreateSerializer
        return SkillsSerializer
    
    def perform_create(self, serializer):
        """Set user when creating skill"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured skills for the user"""
        featured_skills = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_skills, many=True)
        return Response(serializer.data)

class SkillEndorsementViewSet(viewsets.ModelViewSet):
    """ViewSet for Skill Endorsements"""
    
    serializer_class = SkillEndorsementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user_skill__skill']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return endorsements for the current user's skills"""
        return SkillEndorsement.objects.filter(user_skill__user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return SkillEndorsementCreateSerializer
        return SkillEndorsementSerializer
    
    def perform_create(self, serializer):
        """Set endorsed_by when creating endorsement"""
        serializer.save(endorsed_by=self.request.user)

class UserDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for UserDetails model"""
    
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['work_preference', 'employment_type_preference', 'availability']
    search_fields = ['current_job_title', 'desired_job_title', 'industry']
    
    def get_queryset(self):
        """Return user details for the current user"""
        return UserDetails.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return UserDetailsCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserDetailsUpdateSerializer
        return UserDetailsSerializer
    
    def perform_create(self, serializer):
        """Set user when creating user details"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def calculate_completion(self, request, pk=None):
        """Calculate and update profile completion percentage"""
        user_details = self.get_object()
        percentage = user_details.calculate_profile_completion()
        return Response({
            'completion_percentage': percentage,
            'is_complete': percentage >= 80
        })
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment profile views counter"""
        user_details = self.get_object()
        user_details.increment_profile_views()
        return Response({
            'profile_views_count': user_details.profile_views_count
        })
