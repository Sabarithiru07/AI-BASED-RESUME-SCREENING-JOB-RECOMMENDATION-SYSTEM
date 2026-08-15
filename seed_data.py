"""
Seed script — run with: python manage.py shell < seed_data.py
Creates demo users, companies, and job postings.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_ai.settings')

from django.contrib.auth.models import User
from core.models import UserProfile, CompanyProfile, JobPosting

print("🌱 Seeding demo data...")

# ── Company 1: TechCorp ──────────────────────────────────────────────────────
if not User.objects.filter(username='techcorp').exists():
    tc_user = User.objects.create_user(
        username='techcorp', password='demo1234',
        email='hr@techcorp.com', first_name='TechCorp', last_name='HR'
    )
    UserProfile.objects.create(user=tc_user, role='company')
    CompanyProfile.objects.create(
        user=tc_user, company_name='TechCorp Solutions',
        industry='Software Development', location='Bangalore, India',
        company_size='200-500', is_verified=True,
        description='Leading software product company building next-gen SaaS tools.'
    )
    print("✅ Created company: techcorp / demo1234")

# ── Company 2: DataWave ──────────────────────────────────────────────────────
if not User.objects.filter(username='datawave').exists():
    dw_user = User.objects.create_user(
        username='datawave', password='demo1234',
        email='jobs@datawave.io', first_name='DataWave', last_name='Talent'
    )
    UserProfile.objects.create(user=dw_user, role='company')
    CompanyProfile.objects.create(
        user=dw_user, company_name='DataWave Analytics',
        industry='Data & AI', location='Hyderabad, India',
        company_size='50-100', is_verified=True,
        description='Data-driven analytics firm specialising in ML and business intelligence.'
    )
    print("✅ Created company: datawave / demo1234")

# ── Job Seeker 1 ─────────────────────────────────────────────────────────────
if not User.objects.filter(username='alice_dev').exists():
    alice = User.objects.create_user(
        username='alice_dev', password='demo1234',
        email='alice@example.com', first_name='Alice', last_name='Johnson'
    )
    UserProfile.objects.create(user=alice, role='user', phone='+91 9876543210')
    print("✅ Created seeker: alice_dev / demo1234")

# ── Job Seeker 2 ─────────────────────────────────────────────────────────────
if not User.objects.filter(username='bob_ml').exists():
    bob = User.objects.create_user(
        username='bob_ml', password='demo1234',
        email='bob@example.com', first_name='Bob', last_name='Smith'
    )
    UserProfile.objects.create(user=bob, role='user')
    print("✅ Created seeker: bob_ml / demo1234")

# ── Job Postings ──────────────────────────────────────────────────────────────
tc = User.objects.get(username='techcorp')
dw = User.objects.get(username='datawave')

jobs = [
    dict(
        company=tc, title='Senior Python Developer',
        description='We are looking for an experienced Python developer to join our backend team. You will design and build scalable APIs, work closely with DevOps, and mentor junior engineers.',
        requirements='5+ years of Python experience. Strong knowledge of Django or FastAPI. Experience with PostgreSQL and Redis. Familiarity with Docker and CI/CD pipelines.',
        responsibilities='Design RESTful APIs. Code reviews and architectural decisions. Collaborate with frontend and data teams. Write technical documentation.',
        skills_text='python, django, fastapi, postgresql, redis, docker, kubernetes, git, rest api, microservices',
        job_type='full_time', experience_level='senior', location='Bangalore, India',
        salary_min=1800000, salary_max=2800000, status='active'
    ),
    dict(
        company=tc, title='React Frontend Engineer',
        description='Build beautiful and performant web interfaces for our SaaS products. Work with designers and backend engineers in an agile team.',
        requirements='3+ years of React experience. Proficiency in TypeScript. Experience with REST APIs and state management (Redux/Zustand). Strong CSS skills.',
        responsibilities='Develop reusable React components. Optimise frontend performance. Collaborate with UI/UX designers.',
        skills_text='react, typescript, javascript, html, css, redux, webpack, rest api, git, tailwind',
        job_type='full_time', experience_level='mid', location='Remote',
        salary_min=1200000, salary_max=2000000, status='active'
    ),
    dict(
        company=tc, title='DevOps Engineer',
        description='Manage our cloud infrastructure, automate deployments, and ensure high availability of our platform.',
        requirements='3+ years DevOps experience. Hands-on with AWS or GCP. Strong knowledge of Docker and Kubernetes. CI/CD pipeline experience.',
        responsibilities='Manage Kubernetes clusters. Automate infrastructure with Terraform. Monitor systems and on-call support.',
        skills_text='aws, docker, kubernetes, terraform, ansible, jenkins, linux, bash, git, ci/cd, github actions',
        job_type='full_time', experience_level='mid', location='Hyderabad, India',
        salary_min=1500000, salary_max=2400000, status='active'
    ),
    dict(
        company=dw, title='Machine Learning Engineer',
        description='Build and deploy ML models at scale. Work with large datasets and state-of-the-art algorithms to drive business insights.',
        requirements='Strong Python skills. Experience with TensorFlow or PyTorch. Understanding of NLP and computer vision. Familiarity with MLOps tools.',
        responsibilities='Train and evaluate ML models. Deploy models to production. A/B testing and model monitoring.',
        skills_text='python, machine learning, deep learning, tensorflow, pytorch, scikit-learn, pandas, numpy, nlp, docker, aws',
        job_type='full_time', experience_level='mid', location='Hyderabad, India',
        salary_min=1600000, salary_max=2600000, status='active'
    ),
    dict(
        company=dw, title='Data Analyst',
        description='Analyse complex datasets, build dashboards, and deliver actionable insights to our business stakeholders.',
        requirements='2+ years in data analysis. Proficiency in SQL and Python. Experience with Tableau or Power BI. Strong communication skills.',
        responsibilities='Build and maintain dashboards. Perform ad-hoc data analysis. Collaborate with product and engineering teams.',
        skills_text='python, sql, pandas, numpy, tableau, power bi, excel, statistics, data analysis, postgresql',
        job_type='full_time', experience_level='junior', location='Remote',
        salary_min=800000, salary_max=1400000, status='active'
    ),
    dict(
        company=dw, title='NLP Research Engineer',
        description='Research and implement NLP solutions for our text analytics products. Work on LLMs, transformers, and custom language models.',
        requirements='Masters or PhD in CS/ML/Linguistics preferred. Experience with transformers, BERT, GPT. Strong Python skills.',
        responsibilities='Research and prototype NLP models. Fine-tune LLMs for domain-specific tasks. Publish internal research findings.',
        skills_text='nlp, python, pytorch, tensorflow, bert, gpt, machine learning, deep learning, scikit-learn, pandas, numpy',
        job_type='full_time', experience_level='senior', location='Bangalore, India',
        salary_min=2000000, salary_max=3500000, status='active'
    ),
    dict(
        company=tc, title='Python Backend Intern',
        description='Join our engineering team for a 6-month internship. Work on real features, contribute to production code, and learn from senior engineers.',
        requirements='Final year CS/IT student. Basic knowledge of Python and web development. Eagerness to learn.',
        responsibilities='Develop features under guidance. Write unit tests. Participate in code reviews.',
        skills_text='python, django, html, css, git, sql',
        job_type='internship', experience_level='entry', location='Bangalore, India',
        salary_min=25000, salary_max=40000, status='active'
    ),
    dict(
        company=dw, title='Full Stack Developer',
        description='Build end-to-end features across our analytics platform, from backend APIs to frontend dashboards.',
        requirements='4+ years full stack experience. Proficiency in React and Django or Node.js. PostgreSQL and REST API design.',
        responsibilities='Develop full-stack features. Database design and optimisation. Code review and documentation.',
        skills_text='react, django, python, javascript, typescript, postgresql, rest api, docker, git, html, css',
        job_type='full_time', experience_level='mid', location='Chennai, India',
        salary_min=1400000, salary_max=2200000, status='active'
    ),
]

created = 0
for job_data in jobs:
    if not JobPosting.objects.filter(title=job_data['title'], company=job_data['company']).exists():
        JobPosting.objects.create(**job_data)
        created += 1

print(f"✅ Created {created} job postings")
print("\n🎉 Seed complete! Demo credentials:")
print("   Admin:     (your superuser) / (your password)")
print("   Company 1: techcorp  / demo1234")
print("   Company 2: datawave  / demo1234")
print("   Seeker 1:  alice_dev / demo1234")
print("   Seeker 2:  bob_ml    / demo1234")
