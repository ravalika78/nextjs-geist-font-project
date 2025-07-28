import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getai_project.settings')
django.setup()

from jobs.models import Company, Job
from django.contrib.auth.models import User

# Create sample companies
companies_data = [
    {
        'name': 'TechCorp Solutions',
        'description': 'Leading technology company specializing in innovative software solutions and AI development.',
        'location': 'San Francisco, CA',
        'website': 'https://techcorp.com'
    },
    {
        'name': 'DataFlow Systems',
        'description': 'Data analytics and machine learning company helping businesses make data-driven decisions.',
        'location': 'New York, NY',
        'website': 'https://dataflow.io'
    },
    {
        'name': 'CloudTech Inc',
        'description': 'Cloud infrastructure and DevOps solutions provider for modern enterprises.',
        'location': 'Austin, TX',
        'website': 'https://cloudtech.com'
    },
    {
        'name': 'AI Innovations',
        'description': 'Cutting-edge artificial intelligence research and development company.',
        'location': 'Remote',
        'website': 'https://aiinnovations.ai'
    },
    {
        'name': 'StartupHub',
        'description': 'Fast-growing startup ecosystem supporting innovative tech ventures.',
        'location': 'Seattle, WA',
        'website': 'https://startuphub.io'
    }
]

# Create companies
companies = []
for company_data in companies_data:
    company, created = Company.objects.get_or_create(
        name=company_data['name'],
        defaults=company_data
    )
    companies.append(company)

# Create sample jobs
jobs_data = [
    {
        'title': 'Senior Software Engineer',
        'description': 'We are looking for a Senior Software Engineer to join our dynamic team. You will be responsible for designing, developing, and maintaining high-quality software solutions. The ideal candidate has 5+ years of experience in software development and is passionate about building scalable applications.',
        'company': companies[0],
        'location': 'San Francisco, CA',
        'job_type': 'full-time',
        'salary_min': 120000,
        'salary_max': 180000,
        'requirements': '• 5+ years of software development experience\n• Strong proficiency in Python, JavaScript, or similar languages\n• Experience with cloud platforms (AWS, Azure, or GCP)\n• Knowledge of microservices architecture\n• Excellent problem-solving skills\n• Bachelor\'s degree in Computer Science or related field',
        'benefits': '• Competitive salary and equity\n• Health, dental, and vision insurance\n• 401(k) with company match\n• Flexible work arrangements\n• Professional development budget\n• Gym membership'
    },
    {
        'title': 'Data Scientist',
        'description': 'Join our data science team to work on exciting machine learning projects. You will analyze large datasets, build predictive models, and provide actionable insights to drive business decisions.',
        'company': companies[1],
        'location': 'New York, NY',
        'job_type': 'full-time',
        'salary_min': 110000,
        'salary_max': 160000,
        'requirements': '• 3+ years of data science experience\n• Strong Python and SQL skills\n• Experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)\n• Statistical analysis and experimental design knowledge\n• Master\'s degree in Statistics, Mathematics, or related field',
        'benefits': '• Competitive compensation package\n• Comprehensive health benefits\n• Stock options\n• Flexible PTO\n• Conference attendance budget'
    },
    {
        'title': 'DevOps Engineer',
        'description': 'We need a skilled DevOps Engineer to manage our cloud infrastructure and deployment pipelines. You will work with development teams to ensure smooth and reliable software delivery.',
        'company': companies[2],
        'location': 'Austin, TX',
        'job_type': 'full-time',
        'salary_min': 100000,
        'salary_max': 150000,
        'requirements': '• 4+ years of DevOps experience\n• Expertise in AWS, Docker, and Kubernetes\n• CI/CD pipeline development experience\n• Infrastructure as Code (Terraform, CloudFormation)\n• Monitoring and logging tools (Prometheus, ELK stack)\n• Scripting skills in Python or Bash',
        'benefits': '• Remote work options\n• Health and wellness benefits\n• Professional development opportunities\n• Team building events'
    },
    {
        'title': 'Machine Learning Engineer',
        'description': 'Exciting opportunity for a Machine Learning Engineer to work on cutting-edge AI projects. You will design and implement ML models that solve real-world problems.',
        'company': companies[3],
        'location': 'Remote',
        'job_type': 'remote',
        'salary_min': 130000,
        'salary_max': 190000,
        'requirements': '• 3+ years of ML engineering experience\n• Strong Python programming skills\n• Experience with ML frameworks (TensorFlow, PyTorch)\n• Cloud ML platforms (AWS SageMaker, Google AI Platform)\n• MLOps and model deployment experience\n• PhD or Master\'s in Computer Science, ML, or related field',
        'benefits': '• Fully remote work\n• Competitive salary and equity\n• Flexible hours\n• Learning and development budget'
    },
    {
        'title': 'Frontend Developer',
        'description': 'We are seeking a talented Frontend Developer to create beautiful and responsive web applications. You will work with modern JavaScript frameworks to build user-friendly interfaces.',
        'company': companies[4],
        'location': 'Seattle, WA',
        'job_type': 'full-time',
        'salary_min': 90000,
        'salary_max': 140000,
        'requirements': '• 3+ years of frontend development experience\n• Strong JavaScript, HTML, and CSS skills\n• Experience with React, Vue.js, or Angular\n• Responsive design and mobile-first development\n• RESTful API integration experience\n• Git and version control proficiency',
        'benefits': '• Stock options\n• Health insurance\n• Flexible work schedule\n• Modern tech stack'
    },
    {
        'title': 'Product Manager',
        'description': 'Join our product team to drive the strategy and execution of innovative software products. You will work closely with engineering, design, and business stakeholders.',
        'company': companies[0],
        'location': 'San Francisco, CA',
        'job_type': 'full-time',
        'salary_min': 115000,
        'salary_max': 165000,
        'requirements': '• 4+ years of product management experience\n• Strong analytical and strategic thinking skills\n• Experience with agile development methodologies\n• Excellent communication and stakeholder management\n• Data-driven decision making\n• Bachelor\'s degree in Business, Engineering, or related field',
        'benefits': '• Competitive salary and bonus\n• Comprehensive benefits package\n• Career growth opportunities'
    }
]

# Create jobs
for job_data in jobs_data:
    Job.objects.get_or_create(
        title=job_data['title'],
        company=job_data['company'],
        defaults=job_data
    )

print("Sample data created successfully!")
