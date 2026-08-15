from django.contrib import admin
from .models import (
    UserProfile, CompanyProfile, JobPosting, Resume,
    JobApplication, JobRecommendation, Notification, SavedJob, Skill
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_approved', 'created_at']
    list_filter = ['role', 'is_approved']
    search_fields = ['user__username', 'user__email']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'industry']
    search_fields = ['company_name', 'user__username']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'experience_level', 'status', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level']
    search_fields = ['title', 'skills_text']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'experience_years', 'education_level', 'uploaded_at']
    search_fields = ['user__username', 'title']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'ai_score', 'applied_at']
    list_filter = ['status']
    search_fields = ['applicant__username', 'job__title']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']

admin.site.register(JobRecommendation)
admin.site.register(Notification)
admin.site.register(SavedJob)
