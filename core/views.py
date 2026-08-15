from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_POST
from functools import wraps
import json

from .models import (
    UserProfile, CompanyProfile, JobPosting, Resume,
    JobApplication, JobRecommendation, Notification, SavedJob
)
from .forms import (
    RegisterForm, LoginForm, UserProfileForm, CompanyProfileForm,
    JobPostingForm, ResumeUploadForm, JobApplicationForm, ApplicationStatusForm
)
from .nlp_engine import (
    screen_resume, recommend_jobs, extract_text_from_file,
    extract_skills, extract_experience_years, extract_education_level, get_flat_skills
)


# ─── ROLE DECORATORS ─────────────────────────────────────────────────────────

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            profile = getattr(request.user, 'profile', None)
            user_role = profile.role if profile else None
            if request.user.is_superuser:
                user_role = 'admin'
            if user_role not in roles:
                messages.error(request, "Access denied for your role.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_user_role(user):
    if user.is_superuser:
        return 'admin'
    profile = getattr(user, 'profile', None)
    return profile.role if profile else 'user'


def add_notification(user, title, message, ntype='system', link=''):
    Notification.objects.create(
        user=user, title=title, message=message,
        notification_type=ntype, link=link
    )


# ─── PUBLIC VIEWS ────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    stats = {
        'jobs': JobPosting.objects.filter(status='active').count(),
        'companies': CompanyProfile.objects.count(),
        'users': UserProfile.objects.filter(role='user').count(),
        'applications': JobApplication.objects.count(),
    }
    featured_jobs = JobPosting.objects.filter(status='active').order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'stats': stats, 'featured_jobs': featured_jobs})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        role = form.cleaned_data['role']
        profile = UserProfile.objects.create(
            user=user, role=role, phone=form.cleaned_data.get('phone', '')
        )
        if role == 'company':
            CompanyProfile.objects.create(
                user=user, company_name=f"{user.first_name}'s Company"
            )
        login(request, user)
        messages.success(request, f"Welcome, {user.first_name}! Account created successfully.")
        return redirect('dashboard')
    return render(request, 'core/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.first_name or user.username}!")
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'core/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ─── DASHBOARD (ROLE-BASED) ──────────────────────────────────────────────────

@login_required
def dashboard(request):
    role = get_user_role(request.user)
    ctx = {'role': role}

    if role == 'admin':
        ctx.update({
            'total_users': UserProfile.objects.filter(role='user').count(),
            'total_companies': CompanyProfile.objects.count(),
            'total_jobs': JobPosting.objects.count(),
            'total_apps': JobApplication.objects.count(),
            'recent_users': User.objects.filter(profile__role='user').order_by('-date_joined')[:5],
            'recent_jobs': JobPosting.objects.order_by('-created_at')[:5],
            'recent_apps': JobApplication.objects.order_by('-applied_at')[:8],
            'pending_companies': CompanyProfile.objects.filter(is_verified=False).count(),
        })
        return render(request, 'core/admin/dashboard.html', ctx)

    elif role == 'company':
        company_jobs = JobPosting.objects.filter(company=request.user)
        ctx.update({
            'total_jobs': company_jobs.count(),
            'active_jobs': company_jobs.filter(status='active').count(),
            'total_applications': JobApplication.objects.filter(job__company=request.user).count(),
            'shortlisted': JobApplication.objects.filter(job__company=request.user, status='shortlisted').count(),
            'recent_jobs': company_jobs.order_by('-created_at')[:5],
            'recent_applications': JobApplication.objects.filter(
                job__company=request.user
            ).select_related('applicant', 'job').order_by('-applied_at')[:10],
        })
        return render(request, 'core/company/dashboard.html', ctx)

    else:  # user / job seeker
        user_apps = JobApplication.objects.filter(applicant=request.user)
        recs = JobRecommendation.objects.filter(user=request.user).select_related('job')[:6]
        ctx.update({
            'total_applications': user_apps.count(),
            'shortlisted': user_apps.filter(status='shortlisted').count(),
            'interviews': user_apps.filter(status='interview').count(),
            'resumes': request.user.resumes.count(),
            'recommendations': recs,
            'recent_applications': user_apps.select_related('job').order_by('-applied_at')[:6],
            'unread_notifs': request.user.notifications.filter(is_read=False).count(),
        })
        return render(request, 'core/user/dashboard.html', ctx)


# ─── JOB LISTINGS (PUBLIC) ───────────────────────────────────────────────────

def job_list(request):
    jobs = JobPosting.objects.filter(status='active').select_related('company')
    q = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    exp = request.GET.get('exp', '')

    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills_text__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if exp:
        jobs = jobs.filter(experience_level=exp)

    saved_job_ids = set()
    if request.user.is_authenticated:
        saved_job_ids = set(
            SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True)
        )

    return render(request, 'core/job_list.html', {
        'jobs': jobs,
        'saved_job_ids': saved_job_ids,
        'q': q, 'location': location, 'job_type': job_type, 'exp': exp,
        'job_types': JobPosting.JOB_TYPE_CHOICES,
        'exp_levels': JobPosting.EXPERIENCE_CHOICES,
    })


def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    job.views_count += 1
    job.save(update_fields=['views_count'])

    already_applied = False
    is_saved = False
    apply_form = None

    if request.user.is_authenticated and get_user_role(request.user) == 'user':
        already_applied = JobApplication.objects.filter(
            applicant=request.user, job=job
        ).exists()
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
        if not already_applied:
            apply_form = JobApplicationForm(request.user)

    related_jobs = JobPosting.objects.filter(
        status='active'
    ).exclude(pk=pk).filter(
        Q(skills_text__icontains=job.skills_text.split(',')[0] if job.skills_text else '')
        | Q(experience_level=job.experience_level)
    )[:4]

    return render(request, 'core/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'is_saved': is_saved,
        'apply_form': apply_form,
        'related_jobs': related_jobs,
    })


# ─── JOB APPLICATION ─────────────────────────────────────────────────────────

@login_required
@role_required('user')
def apply_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, status='active')
    if JobApplication.objects.filter(applicant=request.user, job=job).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('job_detail', pk=pk)

    form = JobApplicationForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        app = form.save(commit=False)
        app.applicant = request.user
        app.job = job
        app.status = 'screening'
        app.save()

        # Run NLP screening
        if app.resume and app.resume.extracted_text:
            result = screen_resume(app.resume.extracted_text, job)
            app.ai_score = result['score']
            app.ai_feedback = result['feedback']
            app.skill_match_details = result['details']
            app.screened_at = timezone.now()
            app.status = 'applied'
            app.save()

        # Notify company
        if hasattr(job.company, 'company_profile'):
            add_notification(
                job.company,
                f"New Application: {job.title}",
                f"{request.user.get_full_name() or request.user.username} applied for {job.title}.",
                ntype='application',
                link=f'/company/applications/{app.pk}/'
            )

        messages.success(request, f"Applied to {job.title}! AI screening score: {app.ai_score:.0f}%")
        return redirect('my_applications')

    return render(request, 'core/user/apply_job.html', {'form': form, 'job': job})


# ─── MY APPLICATIONS (User) ──────────────────────────────────────────────────

@login_required
@role_required('user')
def my_applications(request):
    apps = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job', 'resume').order_by('-applied_at')
    return render(request, 'core/user/my_applications.html', {'applications': apps})


# ─── RESUME MANAGEMENT ───────────────────────────────────────────────────────

@login_required
@role_required('user')
def resume_list(request):
    resumes = request.user.resumes.all()
    form = ResumeUploadForm()
    return render(request, 'core/user/resume_list.html', {'resumes': resumes, 'form': form})


@login_required
@role_required('user')
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            # Extract text via NLP engine
            text = extract_text_from_file(resume.file.path, resume.file.name)
            resume.extracted_text = text
            resume.skills_extracted = ', '.join(sorted(get_flat_skills(text)))
            resume.experience_years = extract_experience_years(text)
            resume.education_level = extract_education_level(text)
            resume.save()

            # If primary, run recommendations
            if resume.is_primary or request.user.resumes.count() == 1:
                resume.is_primary = True
                resume.save()
                _generate_recommendations(request.user, resume)

            messages.success(request, f"Resume '{resume.title}' uploaded and analysed successfully!")
            return redirect('resume_list')
        else:
            messages.error(request, "Invalid file. Please upload PDF, DOCX, or TXT.")
    return redirect('resume_list')


def _generate_recommendations(user, resume):
    """Generate job recommendations for a user based on their resume."""
    if not resume.extracted_text:
        return
    active_jobs = JobPosting.objects.filter(status='active')
    results = recommend_jobs(resume.extracted_text, active_jobs, top_n=15)
    JobRecommendation.objects.filter(user=user).delete()
    for job, score, reason in results:
        if score > 20:
            JobRecommendation.objects.create(
                user=user, job=job, score=score, reason=reason
            )


@login_required
@role_required('user')
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.file.delete(save=False)
    resume.delete()
    messages.success(request, "Resume deleted.")
    return redirect('resume_list')


# ─── RECOMMENDATIONS ─────────────────────────────────────────────────────────

@login_required
@role_required('user')
def recommendations(request):
    # Refresh recs if resume exists
    primary_resume = request.user.resumes.filter(is_primary=True).first()
    if not primary_resume:
        primary_resume = request.user.resumes.first()
    if primary_resume:
        _generate_recommendations(request.user, primary_resume)

    recs = JobRecommendation.objects.filter(
        user=request.user
    ).select_related('job').order_by('-score')
    JobRecommendation.objects.filter(user=request.user).update(is_viewed=True)
    return render(request, 'core/user/recommendations.html', {
        'recommendations': recs,
        'primary_resume': primary_resume,
    })


# ─── SAVE/UNSAVE JOB ─────────────────────────────────────────────────────────

@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    obj, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        obj.delete()
        return JsonResponse({'saved': False})
    return JsonResponse({'saved': True})


@login_required
@role_required('user')
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'core/user/saved_jobs.html', {'saved_jobs': saved})


# ─── USER PROFILE ────────────────────────────────────────────────────────────

@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(
        request.POST or None, request.FILES or None, instance=profile_obj
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.user.first_name = form.cleaned_data['first_name']
        request.user.last_name = form.cleaned_data.get('last_name', '')
        request.user.email = form.cleaned_data['email']
        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    form.initial = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'core/user/profile.html', {'form': form, 'profile': profile_obj})


# ─── NOTIFICATIONS ────────────────────────────────────────────────────────────

@login_required
def notifications(request):
    notifs = request.user.notifications.all()
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'core/user/notifications.html', {'notifications': notifs})


# ─── COMPANY: JOB MANAGEMENT ─────────────────────────────────────────────────

@login_required
@role_required('company')
def company_jobs(request):
    jobs = JobPosting.objects.filter(company=request.user).annotate(
        app_count=Count('applications')
    )
    return render(request, 'core/company/jobs.html', {'jobs': jobs})


@login_required
@role_required('company')
def create_job(request):
    form = JobPostingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.company = request.user
        job.save()
        messages.success(request, f"Job '{job.title}' posted successfully!")
        return redirect('company_jobs')
    return render(request, 'core/company/create_job.html', {'form': form})


@login_required
@role_required('company')
def edit_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, company=request.user)
    form = JobPostingForm(request.POST or None, instance=job)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Job updated successfully.")
        return redirect('company_jobs')
    return render(request, 'core/company/edit_job.html', {'form': form, 'job': job})


@login_required
@role_required('company')
def delete_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, company=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted.")
        return redirect('company_jobs')
    return render(request, 'core/company/confirm_delete.html', {'job': job})


# ─── COMPANY: APPLICATION MANAGEMENT ─────────────────────────────────────────

@login_required
@role_required('company')
def company_applications(request):
    apps = JobApplication.objects.filter(
        job__company=request.user
    ).select_related('applicant', 'job', 'resume').order_by('-applied_at')

    job_id = request.GET.get('job')
    status = request.GET.get('status')
    if job_id:
        apps = apps.filter(job_id=job_id)
    if status:
        apps = apps.filter(status=status)

    jobs = JobPosting.objects.filter(company=request.user)
    return render(request, 'core/company/applications.html', {
        'applications': apps,
        'jobs': jobs,
        'selected_job': job_id,
        'selected_status': status,
        'status_choices': JobApplication.STATUS_CHOICES,
    })


@login_required
@role_required('company')
def application_detail(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, job__company=request.user)
    form = ApplicationStatusForm(request.POST or None, instance=app)
    if request.method == 'POST' and form.is_valid():
        old_status = app.status
        app = form.save()
        if old_status != app.status:
            add_notification(
                app.applicant,
                f"Application Update: {app.job.title}",
                f"Your application status changed to '{app.get_status_display()}'.",
                ntype='application',
                link='/my-applications/'
            )
        messages.success(request, "Application status updated.")
        return redirect('application_detail', pk=pk)
    return render(request, 'core/company/application_detail.html', {
        'application': app, 'form': form
    })


@login_required
@role_required('company')
def screen_applicant(request, pk):
    """Re-run AI screening on a specific application."""
    app = get_object_or_404(JobApplication, pk=pk, job__company=request.user)
    if app.resume and app.resume.extracted_text:
        result = screen_resume(app.resume.extracted_text, app.job)
        app.ai_score = result['score']
        app.ai_feedback = result['feedback']
        app.skill_match_details = result['details']
        app.screened_at = timezone.now()
        app.save()
        messages.success(request, f"AI screening complete. Score: {app.ai_score:.1f}%")
    else:
        messages.warning(request, "No resume text to screen.")
    return redirect('application_detail', pk=pk)


@login_required
@role_required('company')
def company_profile_view(request):
    profile_obj, _ = CompanyProfile.objects.get_or_create(user=request.user)
    form = CompanyProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Company profile updated.")
        return redirect('company_profile')
    return render(request, 'core/company/company_profile.html', {'form': form, 'company': profile_obj})


# ─── ADMIN VIEWS ─────────────────────────────────────────────────────────────

@login_required
@role_required('admin')
def admin_users(request):
    users = User.objects.filter(profile__role='user').select_related('profile')
    return render(request, 'core/admin/users.html', {'users': users})


@login_required
@role_required('admin')
def admin_companies(request):
    companies = CompanyProfile.objects.select_related('user')
    return render(request, 'core/admin/companies.html', {'companies': companies})


@login_required
@role_required('admin')
def admin_jobs(request):
    jobs = JobPosting.objects.select_related('company').annotate(app_count=Count('applications'))
    return render(request, 'core/admin/jobs.html', {'jobs': jobs})


@login_required
@role_required('admin')
def admin_applications(request):
    apps = JobApplication.objects.select_related('applicant', 'job').order_by('-applied_at')
    return render(request, 'core/admin/applications.html', {'applications': apps})


@login_required
@role_required('admin')
def verify_company(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    company.is_verified = not company.is_verified
    company.save()
    status = "verified" if company.is_verified else "unverified"
    messages.success(request, f"{company.company_name} is now {status}.")
    return redirect('admin_companies')


@login_required
@role_required('admin')
def toggle_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User {user.username} {status}.")
    return redirect('admin_users')


@login_required
@role_required('admin')
def admin_analytics(request):
    from django.db.models.functions import TruncMonth
    monthly_apps = (
        JobApplication.objects
        .annotate(month=TruncMonth('applied_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    score_dist = {
        'excellent': JobApplication.objects.filter(ai_score__gte=75).count(),
        'good': JobApplication.objects.filter(ai_score__gte=50, ai_score__lt=75).count(),
        'fair': JobApplication.objects.filter(ai_score__gte=25, ai_score__lt=50).count(),
        'poor': JobApplication.objects.filter(ai_score__lt=25).count(),
    }
    avg_score = JobApplication.objects.aggregate(avg=Avg('ai_score'))['avg'] or 0
    top_jobs = JobPosting.objects.annotate(app_count=Count('applications')).order_by('-app_count')[:5]
    score_total = sum(score_dist.values())
    score_pct = {
        k: round(v * 100 / score_total, 1) if score_total else 0
        for k, v in score_dist.items()
    }
    return render(request, 'core/admin/analytics.html', {
        'monthly_apps': list(monthly_apps),
        'score_dist': score_dist,
        'score_total': score_total,
        'score_pct': score_pct,
        'avg_score': round(avg_score, 1),
        'top_jobs': top_jobs,
    })
