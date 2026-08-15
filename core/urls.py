from django.urls import path
from . import views

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),

    # ── Auth ────────────────────────────────────────────────────────────────
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    # ── Dashboard ───────────────────────────────────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),

    # ── Job Seeker (user) ───────────────────────────────────────────────────
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/upload/', views.upload_resume, name='upload_resume'),
    path('resumes/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('jobs/<int:pk>/save/', views.toggle_save_job, name='toggle_save_job'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),

    # ── Company ─────────────────────────────────────────────────────────────
    path('company/jobs/', views.company_jobs, name='company_jobs'),
    path('company/jobs/create/', views.create_job, name='create_job'),
    path('company/jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('company/jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('company/applications/', views.company_applications, name='company_applications'),
    path('company/applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('company/applications/<int:pk>/screen/', views.screen_applicant, name='screen_applicant'),
    path('company/profile/', views.company_profile_view, name='company_profile'),

    # ── Admin ────────────────────────────────────────────────────────────────
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:pk>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/companies/', views.admin_companies, name='admin_companies'),
    path('admin-panel/companies/<int:pk>/verify/', views.verify_company, name='verify_company'),
    path('admin-panel/jobs/', views.admin_jobs, name='admin_jobs'),
    path('admin-panel/applications/', views.admin_applications, name='admin_applications'),
    path('admin-panel/analytics/', views.admin_analytics, name='admin_analytics'),
]
