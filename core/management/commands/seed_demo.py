"""
Management command: python manage.py seed_demo

Creates demo users for all three roles + sample jobs + applications.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, CompanyProfile, JobPosting, Resume, JobApplication


DEMO_JOBS = [
    {
        "title": "Senior Python / Django Developer",
        "description": "We are looking for an experienced Python developer to build scalable backend systems. You will work on REST APIs, database design, and cloud deployments.",
        "requirements": "Bachelor's degree in Computer Science or equivalent. 5+ years of Python experience. Strong knowledge of Django, PostgreSQL, and REST APIs.",
        "responsibilities": "Design and implement backend services. Review code and mentor junior developers. Optimize database queries and API performance.",
        "skills_text": "python, django, postgresql, redis, docker, aws, rest api, git",
        "job_type": "full_time",
        "experience_level": "senior",
        "location": "Chennai, India",
        "salary_min": 1200000,
        "salary_max": 1800000,
    },
    {
        "title": "React Frontend Engineer",
        "description": "Join our product team to build beautiful, performant user interfaces. You will work closely with designers and backend engineers.",
        "requirements": "3+ years React experience. Proficiency in TypeScript, CSS-in-JS, and modern frontend tooling.",
        "responsibilities": "Build responsive UI components. Integrate with RESTful APIs. Write unit and integration tests.",
        "skills_text": "react, typescript, javascript, css, html, tailwind, webpack, git, rest api",
        "job_type": "full_time",
        "experience_level": "mid",
        "location": "Bangalore, India",
        "salary_min": 900000,
        "salary_max": 1400000,
    },
    {
        "title": "ML Engineer – NLP Specialist",
        "description": "We are building AI-powered text analysis products. You will design and train NLP models, build data pipelines, and deploy ML services.",
        "requirements": "Master's or PhD in CS, AI, or related field. 3+ years in NLP/ML. Experience with Transformers, BERT, and production ML pipelines.",
        "responsibilities": "Train and fine-tune NLP models. Build evaluation frameworks. Deploy models to production.",
        "skills_text": "python, nlp, machine learning, deep learning, pytorch, tensorflow, bert, scikit-learn, pandas, numpy",
        "job_type": "full_time",
        "experience_level": "mid",
        "location": "Remote",
        "salary_min": 1500000,
        "salary_max": 2200000,
    },
    {
        "title": "DevOps / Cloud Engineer",
        "description": "Help us build and maintain scalable infrastructure on AWS. You will manage CI/CD pipelines, container orchestration, and monitoring.",
        "requirements": "3+ years in DevOps or SRE. Strong AWS and Kubernetes experience. Proficiency in Terraform and Ansible.",
        "responsibilities": "Manage Kubernetes clusters. Build automated deployment pipelines. Implement observability and alerting.",
        "skills_text": "aws, kubernetes, docker, terraform, ansible, linux, ci/cd, jenkins, github actions, nginx",
        "job_type": "full_time",
        "experience_level": "mid",
        "location": "Hyderabad, India",
        "salary_min": 1000000,
        "salary_max": 1600000,
    },
    {
        "title": "Full Stack Developer (Node + React)",
        "description": "We need a versatile full-stack developer to own features end-to-end. You will build APIs in Node.js and UIs in React.",
        "requirements": "3+ years of full-stack development. Proficiency in Node.js, Express, React, and MongoDB or PostgreSQL.",
        "responsibilities": "Build full-stack features. Design database schemas. Participate in sprint planning and reviews.",
        "skills_text": "javascript, node.js, react, express, mongodb, postgresql, html, css, git, rest api",
        "job_type": "full_time",
        "experience_level": "mid",
        "location": "Mumbai, India",
        "salary_min": 800000,
        "salary_max": 1300000,
    },
    {
        "title": "Data Analyst",
        "description": "Analyse business metrics, build dashboards, and provide actionable insights to product and marketing teams.",
        "requirements": "Bachelor's in Statistics, Math, or Computer Science. 2+ years of data analysis experience. Proficiency in SQL and Python.",
        "responsibilities": "Build Tableau/Power BI dashboards. Write complex SQL queries. Present insights to stakeholders.",
        "skills_text": "python, sql, pandas, numpy, tableau, power bi, excel, statistics, data analysis",
        "job_type": "full_time",
        "experience_level": "junior",
        "location": "Pune, India",
        "salary_min": 600000,
        "salary_max": 1000000,
    },
    {
        "title": "Android Developer (Kotlin)",
        "description": "Build and maintain our Android mobile application used by millions of users.",
        "requirements": "2+ years Android development with Kotlin. Experience with Jetpack Compose and MVVM architecture.",
        "responsibilities": "Develop new features for the Android app. Fix bugs and improve performance. Write unit tests.",
        "skills_text": "android, kotlin, jetpack compose, mvvm, retrofit, room, git",
        "job_type": "full_time",
        "experience_level": "junior",
        "location": "Delhi, India",
        "salary_min": 700000,
        "salary_max": 1100000,
    },
    {
        "title": "Cybersecurity Analyst",
        "description": "Protect our infrastructure and products from security threats. Perform penetration testing, vulnerability assessments, and incident response.",
        "requirements": "Bachelor's in Cybersecurity or Computer Science. 3+ years in security. CISSP or CEH certification preferred.",
        "responsibilities": "Conduct security audits. Monitor for threats and incidents. Develop security policies.",
        "skills_text": "cybersecurity, penetration testing, linux, python, network security, siem, firewall, incident response",
        "job_type": "full_time",
        "experience_level": "mid",
        "location": "Remote",
        "salary_min": 1100000,
        "salary_max": 1700000,
    },
]

DEMO_RESUME_TEXT = """
John Doe
Senior Software Engineer
john.doe@email.com | +91 9876543210 | Chennai, India

SUMMARY
Experienced software engineer with 5 years of professional experience in building scalable
web applications using Python, Django, React, and PostgreSQL. Passionate about clean code
and AI/ML applications.

EXPERIENCE
Senior Software Engineer | TechCorp India | 2021 - Present
- Developed REST APIs using Django and PostgreSQL serving 1M+ requests/day
- Built React frontend components with TypeScript and Redux
- Containerized applications with Docker and deployed to AWS ECS
- Led a team of 4 junior developers

Software Engineer | StartupXYZ | 2019 - 2021
- Built full-stack features using Python, Django, and Vue.js
- Designed database schemas for PostgreSQL
- Integrated third-party APIs and payment gateways

EDUCATION
Bachelor of Technology in Computer Science
Anna University, Chennai | 2015 - 2019

SKILLS
Programming: Python, JavaScript, TypeScript, SQL
Frameworks: Django, Flask, React, Node.js
Databases: PostgreSQL, MySQL, Redis, MongoDB
DevOps: Docker, Kubernetes, AWS, CI/CD, Git
Machine Learning: scikit-learn, pandas, numpy, NLP

CERTIFICATIONS
- AWS Certified Developer Associate
- Python Professional Certificate
"""


class Command(BaseCommand):
    help = 'Seed the database with demo users and job data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding demo data...'))

        # ── Admin user ──────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@talentai.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})
            self.stdout.write(self.style.SUCCESS('  ✅ Admin: admin / admin123'))

        # ── Company user ──────────────────────────────────────────────────
        if not User.objects.filter(username='techcorp').exists():
            company_user = User.objects.create_user(
                username='techcorp',
                email='hr@techcorp.com',
                password='company123',
                first_name='TechCorp',
                last_name='HR'
            )
            UserProfile.objects.get_or_create(user=company_user, defaults={'role': 'company'})
            CompanyProfile.objects.get_or_create(
                user=company_user,
                defaults={
                    'company_name': 'TechCorp India',
                    'industry': 'Software & Technology',
                    'location': 'Chennai, India',
                    'website': 'https://techcorp.example.com',
                    'company_size': '200-500 employees',
                    'description': 'TechCorp India is a leading software company specializing in enterprise SaaS products, cloud solutions, and AI-powered analytics.',
                    'founded_year': 2012,
                    'is_verified': True,
                }
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Company: techcorp / company123'))
        else:
            company_user = User.objects.get(username='techcorp')

        # ── Second company ──────────────────────────────────────────────────
        if not User.objects.filter(username='innovateai').exists():
            company2 = User.objects.create_user(
                username='innovateai',
                email='hr@innovateai.com',
                password='company123',
                first_name='InnovateAI',
                last_name='HR'
            )
            UserProfile.objects.get_or_create(user=company2, defaults={'role': 'company'})
            CompanyProfile.objects.get_or_create(
                user=company2,
                defaults={
                    'company_name': 'InnovateAI Solutions',
                    'industry': 'Artificial Intelligence',
                    'location': 'Bangalore, India',
                    'company_size': '50-200 employees',
                    'description': 'InnovateAI builds cutting-edge AI and machine learning products for enterprises across India and Southeast Asia.',
                    'founded_year': 2018,
                    'is_verified': True,
                }
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Company2: innovateai / company123'))
        else:
            company2 = User.objects.get(username='innovateai')

        # ── Job seeker ───────────────────────────────────────────────────────
        if not User.objects.filter(username='jobseeker').exists():
            seeker = User.objects.create_user(
                username='jobseeker',
                email='john.doe@email.com',
                password='seeker123',
                first_name='John',
                last_name='Doe'
            )
            UserProfile.objects.get_or_create(user=seeker, defaults={'role': 'user', 'phone': '+91 9876543210'})
            self.stdout.write(self.style.SUCCESS('  ✅ Seeker: jobseeker / seeker123'))
        else:
            seeker = User.objects.get(username='jobseeker')

        # ── Jobs ─────────────────────────────────────────────────────────────
        if JobPosting.objects.count() == 0:
            companies = [company_user, company2, company_user, company2,
                         company_user, company2, company_user, company2]
            for i, job_data in enumerate(DEMO_JOBS):
                JobPosting.objects.create(
                    company=companies[i % len(companies)],
                    status='active',
                    **job_data
                )
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(DEMO_JOBS)} demo jobs'))

        # ── Resume ──────────────────────────────────────────────────────────
        if not seeker.resumes.exists():
            import tempfile, os
            from django.core.files.base import ContentFile
            resume = Resume(
                user=seeker,
                title='John Doe - Senior Software Engineer',
                is_primary=True,
                extracted_text=DEMO_RESUME_TEXT,
                skills_extracted='python, django, react, postgresql, docker, aws, typescript, redis, machine learning, nlp',
                experience_years=5,
                education_level='bachelors',
            )
            resume.file.save('demo_resume.txt', ContentFile(DEMO_RESUME_TEXT.encode()), save=True)
            self.stdout.write(self.style.SUCCESS('  ✅ Demo resume created'))

            # Generate recommendations
            from core.nlp_engine import recommend_jobs
            from core.models import JobRecommendation
            jobs = JobPosting.objects.filter(status='active')
            results = recommend_jobs(DEMO_RESUME_TEXT, jobs, top_n=8)
            for job, score, reason in results:
                if score > 15:
                    JobRecommendation.objects.get_or_create(
                        user=seeker, job=job,
                        defaults={'score': score, 'reason': reason}
                    )
            self.stdout.write(self.style.SUCCESS(f'  ✅ Generated {len(results)} AI recommendations'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data seeded successfully!\n'))
        self.stdout.write('  Login credentials:')
        self.stdout.write('  ┌─────────────────────────────────────────────────┐')
        self.stdout.write('  │  Admin    → username: admin      pw: admin123   │')
        self.stdout.write('  │  Company  → username: techcorp   pw: company123 │')
        self.stdout.write('  │  Company2 → username: innovateai pw: company123 │')
        self.stdout.write('  │  Seeker   → username: jobseeker  pw: seeker123  │')
        self.stdout.write('  └─────────────────────────────────────────────────┘\n')
