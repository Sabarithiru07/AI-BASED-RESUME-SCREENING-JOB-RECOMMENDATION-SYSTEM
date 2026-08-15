# 🧠 TalentAI — AI-Powered Resume Screening & Job Recommendation System

A professional Django web application with NLP-based resume screening and intelligent job recommendations. Built with a pure Python NLP engine (no external ML dependencies required).

---

## 🚀 Features

### 🤖 AI / NLP Engine
- **TF-IDF Cosine Similarity** — Measures how well a resume matches job content
- **Skill Taxonomy Matching** — 400+ skills across 9 categories (Python, DevOps, ML, etc.)
- **Experience Extraction** — Regex-based years-of-experience detection
- **Education Detection** — Identifies PhD, Masters, Bachelors, Diploma from text
- **AI Match Score (0–100%)** — Weighted composite score for every application
- **Smart Job Recommendations** — Personalised job feed based on uploaded resume

### 👥 Three-Role Authentication
| Role | Access |
|------|--------|
| **Admin** (superuser) | Manage all users, companies, jobs, analytics |
| **Company / Recruiter** | Post jobs, view AI-screened applicants, update status |
| **Job Seeker** | Upload resumes, apply to jobs, get AI recommendations |

### 📄 Resume Handling
- Upload PDF, DOCX, or TXT files (up to 10 MB)
- Automatic text extraction
- Skill, education, and experience parsing
- Primary resume used for job recommendations

### 🏢 Company Portal
- Full job posting management (create, edit, delete, pause)
- AI screening report per application (skill match, content similarity, experience gap)
- Re-screen candidates with one click
- Manage application pipeline (Applied → Shortlisted → Interview → Offered/Rejected)

---

## 📁 Project Structure

```
resume_ai/                      ← Django project root
├── manage.py
├── requirements.txt
├── resume_ai/                  ← Project settings package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                       ← Single app (all features)
    ├── models.py               ← All database models
    ├── views.py                ← All views (admin, company, user)
    ├── forms.py                ← All forms
    ├── urls.py                 ← All URL routes
    ├── admin.py                ← Django admin config
    ├── nlp_engine.py           ← 🧠 Pure-Python NLP/AI engine
    ├── migrations/
    └── templates/core/
        ├── base.html           ← Sidebar layout + dark theme
        ├── home.html           ← Public landing page
        ├── job_list.html       ← Browse + filter jobs
        ├── job_detail.html     ← Job detail + apply
        ├── auth/               ← Login, Register
        ├── user/               ← Dashboard, Resumes, Applications, Recommendations
        ├── company/            ← Dashboard, Jobs, Applications, AI Screening
        └── admin/              ← Users, Companies, Jobs, Analytics
```

---

## ⚙️ Setup Instructions

### 1. Clone / extract the project
```bash
cd resume_ai
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (Admin)
```bash
python manage.py createsuperuser
```
After creating, run this to assign the admin profile:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from core.models import UserProfile
>>> u = User.objects.get(username='your_superuser_username')
>>> UserProfile.objects.get_or_create(user=u, defaults={'role': 'admin'})
>>> exit()
```

### 6. Load sample data (optional)
```bash
python manage.py shell < seed_data.py
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🔗 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Public landing page |
| `/auth/login/` | Login |
| `/auth/register/` | Register (Job Seeker or Company) |
| `/dashboard/` | Role-based dashboard |
| `/jobs/` | Browse all jobs |
| `/recommendations/` | AI job recommendations |
| `/resumes/` | Upload & manage resumes |
| `/my-applications/` | Track application statuses |
| `/company/jobs/` | Company: manage jobs |
| `/company/applications/` | Company: view all applicants + AI scores |
| `/admin-panel/analytics/` | Admin: platform analytics |
| `/django-admin/` | Django admin panel |

---

## 🧠 NLP Engine — How It Works

```
Resume Text + Job Description
         │
         ▼
┌─────────────────────────────┐
│   1. Text Preprocessing     │  Lowercase, tokenize, remove stopwords
│   2. TF-IDF Vectors         │  Term frequency × inverse document frequency
│   3. Cosine Similarity      │  How similar are resume & job? (35% weight)
│   4. Skill Taxonomy Match   │  400+ skills in 9 categories (40% weight)
│   5. Experience Detection   │  Regex: "5+ years experience" (15% weight)
│   6. Education Detection    │  PhD=5, Masters=4, Bachelors=3 ... (10% weight)
└─────────────────────────────┘
         │
         ▼
   AI Match Score (0–100)
   + Detailed Feedback
   + Matched/Missing Skills
```

**Score Interpretation:**
- 🟢 ≥75% — Excellent Match (strongly recommended)
- 🔵 50–74% — Good Match
- 🟡 25–49% — Fair Match
- 🔴 <25% — Poor Match

---

## 🎨 Design

- **Dark theme** with deep blue/indigo accent palette
- **Syne** (display) + **DM Sans** (body) fonts
- Responsive sidebar layout
- Role-coloured stat cards, AI score rings, skill tags
- Smooth hover transitions and progress bars

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| NLP Engine | Pure Python (TF-IDF, cosine similarity) |
| PDF Parsing | pypdf / PyPDF2 |
| DOCX Parsing | python-docx |
| Frontend | Vanilla HTML/CSS/JS (no React needed) |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts (Syne + DM Sans) |

---

## 🔒 Production Checklist

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Switch to PostgreSQL database
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up media file serving (S3 or similar)
- [ ] Add `python-decouple` for environment variables

---

## 📝 License

MIT License — Free to use, modify, and distribute.
