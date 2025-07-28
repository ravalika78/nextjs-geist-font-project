from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job, Company, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializer, CompanySerializer

def home(request):
    """Home page with featured jobs and search functionality"""
    featured_jobs = Job.objects.filter(is_active=True)[:6]
    context = {
        'featured_jobs': featured_jobs,
    }
    return render(request, 'jobs/home.html', context)

def job_list(request):
    """List all jobs with search and filtering"""
    jobs = Job.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'location': location,
        'job_type': job_type,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    """Detailed view of a specific job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_detail.html', context)

def company_list(request):
    """List all companies"""
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'jobs/company_list.html', context)

def company_detail(request, company_id):
    """Detailed view of a specific company"""
    company = get_object_or_404(Company, id=company_id)
    company_jobs = company.jobs.filter(is_active=True)
    context = {
        'company': company,
        'company_jobs': company_jobs,
    }
    return render(request, 'jobs/company_detail.html', context)

@login_required
def profile(request):
    """User profile page"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, 'jobs/profile.html', context)

@login_required
def apply_job(request, job_id):
    """Apply for a job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    if request.method == 'POST':
        # Handle job application form submission
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')
        
        if resume:
            from .models import JobApplication
            application = JobApplication.objects.create(
                user=request.user,
                job=job,
                resume=resume,
                cover_letter=cover_letter
            )
            return render(request, 'jobs/application_success.html', {'job': job})
    
    return render(request, 'jobs/apply_job.html', {'job': job})

# API Views
@api_view(['GET'])
def api_job_list(request):
    """API endpoint for job list"""
    jobs = Job.objects.filter(is_active=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_job_detail(request, job_id):
    """API endpoint for job detail"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    serializer = JobSerializer(job)
    return Response(serializer.data)

@api_view(['GET'])
def api_company_list(request):
    """API endpoint for company list"""
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_company_detail(request, company_id):
    """API endpoint for company detail"""
    company = get_object_or_404(Company, id=company_id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)

def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        jobs = Job.objects.filter(
            Q(title__icontains=query) | 
            Q(company__name__icontains=query)
        ).filter(is_active=True)[:5]
        
        suggestions = []
        for job in jobs:
            suggestions.append({
                'title': job.title,
                'company': job.company.name,
                'location': job.location,
                'url': f'/jobs/{job.id}/'
            })
        
        return JsonResponse({'suggestions': suggestions})
    
    return JsonResponse({'suggestions': []})
