from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    EducationViewSet,
    ExperienceViewSet,
    RegisterViewSet,
    ResumeViewSet,
    SkillCategoryViewSet,
    SkillViewSet,
    SkillsViewSet,
    SkillEndorsementViewSet,
    UserDetailsViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'education', EducationViewSet, basename='education')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'skill-categories', SkillCategoryViewSet, basename='skillcategory')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'user-skills', SkillsViewSet, basename='userskills')
router.register(r'skill-endorsements', SkillEndorsementViewSet, basename='skillendorsement')
router.register(r'user-details', UserDetailsViewSet, basename='userdetails')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Login/logout for browsable API
]
