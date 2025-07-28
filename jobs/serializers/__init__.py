from .education_serializer import EducationSerializer
from .experience_serializer import ExperienceSerializer
from .register_serializer import RegisterSerializer
from .resume_serializer import ResumeSerializer
from .skills_serializer import SkillSerializer, SkillsSerializer, SkillEndorsementSerializer, SkillCategorySerializer
from .userdetails_serializer import UserDetailsSerializer

__all__ = [
    'EducationSerializer',
    'ExperienceSerializer',
    'RegisterSerializer',
    'ResumeSerializer',
    'SkillSerializer',
    'SkillsSerializer',
    'SkillEndorsementSerializer',
    'SkillCategorySerializer',
    'UserDetailsSerializer',
]
