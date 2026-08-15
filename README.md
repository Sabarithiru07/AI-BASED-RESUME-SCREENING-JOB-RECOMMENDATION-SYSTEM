<<<<<<< HEAD
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
=======
# AI-BASED-RESUME-SCREENING-JOB-RECOMMENDATION-SYSTEM

The AI Resume Screening and Job Recommendation system is designed to automatically analyze candidate resumes and match them with relevant job postings using natural language processing techniques. It processes resumes by cleaning and tokenizing text, generating n-grams, and removing stop words, then extracts skills based on a comprehensive skill taxonomy covering technical, domain-specific, and soft skills. The system identifies the candidate’s highest education level and calculates years of professional experience using regex-based patterns. It compares resumes to job descriptions using TF-IDF vectorization and cosine similarity, evaluates skill matches, and measures alignment with required education and experience. A weighted scoring mechanism combines these factors into a final compatibility score, accompanied by human-readable feedback highlighting matched skills, gaps, and strengths. Additionally, the system recommends jobs by ranking multiple postings against a candidate’s profile, providing scores and explanations for each recommendation. Resume text extraction supports TXT, PDF, and DOCX formats, ensuring robust preprocessing. Overall, this system offers an end-to-end AI solution for recruitment, enabling efficient candidate evaluation, actionable feedback, and intelligent job recommendations.

<img width="1358" height="643" alt="33f1f0ca-c85c-4822-ac68-7212be189fae_20260406_2884326388249718878" src="https://github.com/user-attachments/assets/67e442c7-a8c5-45dd-9286-ec16f801dda5" />

<img width="1356" height="642" alt="33f1f0ca-c85c-4822-ac68-7212be189fae_20260406_9058740467423368257" src="https://github.com/user-attachments/assets/99f8fb57-282b-4944-985a-757aa239fee3" />

<img width="1357" height="644" alt="33f1f0ca-c85c-4822-ac68-7212be189fae_20260406_7904162660112942291" src="https://github.com/user-attachments/assets/a15bfaab-68dd-4f5f-b095-f0d9271cc80f" />

<img width="1358" height="640" alt="33f1f0ca-c85c-4822-ac68-7212be189fae_20260406_2416708108612847741" src="https://github.com/user-attachments/assets/afad5ffd-710c-4ec5-a0de-b21190edf655" />

<img width="1353" height="647" alt="33f1f0ca-c85c-4822-ac68-7212be189fae_20260406_6143816899688838421" src="https://github.com/user-attachments/assets/cb678fc4-882d-4132-bcd3-1af5cbaec1df" />

>>>>>>> 44ad5c0d8b527acf4726910de090e91015dfc69a
