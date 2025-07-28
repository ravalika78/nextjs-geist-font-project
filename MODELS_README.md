# GET-AI Django Models & API Structure

## Overview
This project has been restructured to use a modular approach with separate model files and corresponding serializers/viewsets for a comprehensive job search platform.

## 📁 Model Structure

### Models Folder (`jobs/models/`)
- **education.py**: User education history
- **experience.py**: Work experience records
- **register.py**: Extended user registration/profile
- **resume.py**: Resume management with version control
- **skills.py**: Skills system with categories and endorsements
- **userdetails.py**: Comprehensive user details and preferences

### Serializers Folder (`jobs/serializers/`)
Each model has dedicated serializers with:
- Basic serializers for read operations
- Create serializers for POST requests
- Update serializers for PUT/PATCH requests
- Custom validation and computed fields

### ViewSets (`jobs/viewsets.py`)
RESTful API endpoints for all models with:
- CRUD operations
- Filtering and search
- Custom actions
- Permission-based access

## 🔗 API Endpoints

### Base URL: `http://localhost:8000/api/v1/`

#### Education
- `GET/POST /api/v1/education/` - List/Create education entries
- `GET/PUT/PATCH/DELETE /api/v1/education/{id}/` - Individual education management

#### Experience
- `GET/POST /api/v1/experience/` - List/Create work experience
- `GET/PUT/PATCH/DELETE /api/v1/experience/{id}/` - Individual experience management

#### Registration
- `GET/POST /api/v1/register/` - User registration profile
- `POST /api/v1/register/{id}/check_completeness/` - Check profile completeness

#### Resume Management
- `GET/POST /api/v1/resume/` - List/Create resumes
- `POST /api/v1/resume/{id}/download/` - Track downloads
- `POST /api/v1/resume/{id}/set_primary/` - Set as primary resume

#### Skills System
- `GET /api/v1/skill-categories/` - Browse skill categories
- `GET /api/v1/skills/` - Browse available skills
- `GET/POST /api/v1/user-skills/` - Manage user skills
- `GET/POST /api/v1/skill-endorsements/` - Skill endorsements

#### User Details
- `GET/POST /api/v1/user-details/` - Comprehensive user details
- `POST /api/v1/user-details/{id}/calculate_completion/` - Calculate profile completion
- `POST /api/v1/user-details/{id}/increment_views/` - Track profile views

## 🛠️ Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 📊 Model Relationships

```
User (Django built-in)
├── Register (1:1) - Extended profile
├── Education (1:N) - Education history
├── Experience (1:N) - Work experience
├── Resume (1:N) - Resume versions
├── Skills (1:N) - User skills
├── SkillEndorsement (1:N) - Given endorsements
└── UserDetails (1:1) - Comprehensive details

SkillCategory (1:N) Skill
Skill (1:N) Skills (user skills)
Skills (1:N) SkillEndorsement
```

## 🔐 Authentication
All API endpoints require authentication. Use:
- Session authentication for web interface
- Token authentication for API clients
- Admin interface at `/admin/`

## 📋 Admin Interface
Access the admin interface at `http://localhost:8000/admin/` to manage all models.

## 🎯 Features

### Resume Management
- Multiple resume versions
- Primary resume selection
- Download tracking
- File type validation
- Size limits

### Skills System
- Skill categories
- Proficiency levels
- Endorsements
- Trending skills
- Verification status

### User Profile
- Complete profile tracking
- Privacy settings
- Notification preferences
- Career preferences
- Location preferences

### Education & Experience
- Comprehensive records
- Duration calculations
- Validation rules
- Search and filtering

## 🚀 Next Steps

1. Run migrations for new models
2. Register new admin configurations
3. Test API endpoints
4. Add frontend integration
5. Implement additional features like:
   - AI-powered resume parsing
   - Skill recommendations
   - Job matching algorithms
   - Real-time notifications
