from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ─── USER ROLE PROFILE ───────────────────────────────────────────────────────

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('company', 'Job Poster / Company'),
        ('user', 'Job Seeker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ─── COMPANY PROFILE ─────────────────────────────────────────────────────────

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# ─── SKILLS ──────────────────────────────────────────────────────────────────

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


# ─── JOB POSTING ─────────────────────────────────────────────────────────────

class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]

    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-1 yrs)'),
        ('junior', 'Junior (1-3 yrs)'),
        ('mid', 'Mid Level (3-5 yrs)'),
        ('senior', 'Senior (5-8 yrs)'),
        ('lead', 'Lead / Principal (8+ yrs)'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField(blank=True)
    skills_required = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    skills_text = models.TextField(blank=True, help_text='Comma-separated skills for NLP matching')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='mid')
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company.company_profile.company_name if hasattr(self.company, 'company_profile') else self.company.username}"

    def get_salary_display(self):
        if self.salary_min and self.salary_max:
            return f"₹{self.salary_min:,.0f} - ₹{self.salary_max:,.0f}"
        elif self.salary_min:
            return f"From ₹{self.salary_min:,.0f}"
        return "Negotiable"


# ─── RESUME ───────────────────────────────────────────────────────────────────

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, default='My Resume')
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    skills_extracted = models.TextField(blank=True)
    experience_years = models.FloatField(default=0)
    education_level = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_screened = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ─── JOB APPLICATION ─────────────────────────────────────────────────────────

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'AI Screening'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    ai_score = models.FloatField(default=0)  # 0-100 match score
    ai_feedback = models.TextField(blank=True)
    skill_match_details = models.JSONField(default=dict, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    screened_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('applicant', 'job')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"

    def get_score_class(self):
        if self.ai_score >= 75:
            return 'excellent'
        elif self.ai_score >= 50:
            return 'good'
        elif self.ai_score >= 25:
            return 'fair'
        return 'poor'


# ─── JOB RECOMMENDATION ──────────────────────────────────────────────────────

class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(default=0)
    reason = models.TextField(blank=True)
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-score']

    def __str__(self):
        return f"Rec: {self.user.username} → {self.job.title} ({self.score:.1f})"


# ─── NOTIFICATION ─────────────────────────────────────────────────────────────

class Notification(models.Model):
    TYPE_CHOICES = [
        ('application', 'Application Update'),
        ('recommendation', 'New Recommendation'),
        ('shortlist', 'Shortlisted'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


# ─── SAVED JOBS ───────────────────────────────────────────────────────────────

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
