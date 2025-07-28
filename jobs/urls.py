from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('profile/', views.profile, name='profile'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    
    # API endpoints
    path('api/jobs/', views.api_job_list, name='api_job_list'),
    path('api/jobs/<int:job_id>/', views.api_job_detail, name='api_job_detail'),
    path('api/companies/', views.api_company_list, name='api_company_list'),
    path('api/companies/<int:company_id>/', views.api_company_detail, name='api_company_detail'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
]
