"""
AI/NLP Engine for Resume Screening and Job Recommendation
Uses: TF-IDF, Cosine Similarity, Keyword Extraction, Skill Matching
"""
import re
import math
import json
from collections import Counter


# ─── SKILL TAXONOMY ──────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    'programming': [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'php', 'typescript', 'scala', 'r', 'matlab',
        'perl', 'bash', 'shell', 'powershell', 'dart', 'lua', 'elixir'
    ],
    'web_frontend': [
        'react', 'angular', 'vue', 'html', 'css', 'sass', 'less', 'bootstrap',
        'tailwind', 'jquery', 'webpack', 'vite', 'next.js', 'nuxt', 'gatsby',
        'redux', 'graphql', 'rest api', 'responsive design', 'figma'
    ],
    'web_backend': [
        'django', 'flask', 'fastapi', 'node.js', 'express', 'spring', 'laravel',
        'rails', 'asp.net', 'gin', 'fiber', 'nestjs', 'strapi', 'microservices'
    ],
    'database': [
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite',
        'oracle', 'mssql', 'cassandra', 'dynamodb', 'firebase', 'supabase',
        'neo4j', 'influxdb', 'mariadb'
    ],
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible',
        'jenkins', 'ci/cd', 'github actions', 'linux', 'nginx', 'apache',
        'devops', 'cloud', 'serverless', 'microservices', 'helm'
    ],
    'data_ml': [
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
        'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy',
        'data science', 'neural network', 'ai', 'llm', 'bert', 'gpt',
        'data analysis', 'statistics', 'tableau', 'power bi', 'excel'
    ],
    'mobile': [
        'android', 'ios', 'react native', 'flutter', 'swift', 'kotlin',
        'xamarin', 'ionic', 'capacitor'
    ],
    'soft_skills': [
        'leadership', 'communication', 'teamwork', 'problem solving', 'agile',
        'scrum', 'project management', 'time management', 'critical thinking',
        'collaboration', 'mentoring', 'presentation', 'analytical'
    ],
}

EDUCATION_LEVELS = {
    'phd': ['phd', 'doctorate', 'doctoral', 'ph.d'],
    'masters': ['master', 'msc', 'm.sc', 'mba', 'm.tech', 'me', 'ms', 'mca'],
    'bachelors': ['bachelor', 'bsc', 'b.sc', 'btech', 'b.tech', 'be', 'ba', 'bca', 'b.e'],
    'diploma': ['diploma', 'associate', 'certificate'],
    'highschool': ['high school', '12th', 'hsc', 'sslc', '10th'],
}

EDUCATION_WEIGHTS = {'phd': 5, 'masters': 4, 'bachelors': 3, 'diploma': 2, 'highschool': 1}

STOP_WORDS = {
    'a', 'an', 'the', 'is', 'in', 'it', 'of', 'to', 'and', 'or', 'for',
    'on', 'at', 'by', 'with', 'as', 'from', 'was', 'are', 'be', 'been',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'not', 'no', 'nor', 'so',
    'yet', 'both', 'either', 'neither', 'each', 'than', 'that', 'this',
    'these', 'those', 'such', 'only', 'own', 'same', 'too', 'very',
    'just', 'but', 'also', 'up', 'about', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
    'under', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'any', 'most', 'other', 'some', 'more', 'we', 'our', 'you', 'he',
    'she', 'they', 'i', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
}


# ─── TEXT PREPROCESSING ──────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Lowercase, remove special chars, normalize whitespace."""
    text = text.lower()
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> list:
    """Split into tokens, remove stop words."""
    tokens = clean_text(text).split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def get_ngrams(tokens: list, n: int = 2) -> list:
    """Generate n-grams."""
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


# ─── SKILL EXTRACTION ────────────────────────────────────────────────────────

def extract_skills(text: str) -> dict:
    """Extract skills from text using keyword matching across taxonomy."""
    text_lower = clean_text(text)
    found = {}
    for category, skills in SKILL_TAXONOMY.items():
        matched = []
        for skill in skills:
            # Match whole words / phrases
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(skill)
        if matched:
            found[category] = matched
    return found


def get_flat_skills(text: str) -> set:
    """Return flat set of all extracted skills."""
    skills_by_cat = extract_skills(text)
    flat = set()
    for skills in skills_by_cat.values():
        flat.update(skills)
    return flat


# ─── EDUCATION EXTRACTION ────────────────────────────────────────────────────

def extract_education_level(text: str) -> str:
    """Determine highest education level from text."""
    text_lower = text.lower()
    for level in ['phd', 'masters', 'bachelors', 'diploma', 'highschool']:
        for keyword in EDUCATION_LEVELS[level]:
            if keyword in text_lower:
                return level
    return 'unknown'


# ─── EXPERIENCE EXTRACTION ───────────────────────────────────────────────────

def extract_experience_years(text: str) -> float:
    """Extract years of experience using regex patterns."""
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s+(?:of\s+)?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
        r'(\d{4})\s*[-–]\s*(\d{4}|present|current)',
    ]
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            if isinstance(match, tuple):
                try:
                    if match[1].lower() in ('present', 'current'):
                        from datetime import datetime
                        yrs = datetime.now().year - int(match[0])
                        years.append(yrs)
                    else:
                        years.append(abs(int(match[1]) - int(match[0])))
                except:
                    pass
            else:
                try:
                    years.append(int(match))
                except:
                    pass
    return max(years) if years else 0


# ─── TF-IDF IMPLEMENTATION ───────────────────────────────────────────────────

def compute_tf(tokens: list) -> dict:
    """Term frequency."""
    if not tokens:
        return {}
    counter = Counter(tokens)
    total = len(tokens)
    return {word: count / total for word, count in counter.items()}


def compute_tfidf_vector(text: str, idf: dict = None) -> dict:
    """Compute TF-IDF vector for a document."""
    tokens = tokenize(text)
    bigrams = get_ngrams(tokens, 2)
    all_tokens = tokens + bigrams
    tf = compute_tf(all_tokens)
    if idf is None:
        return tf
    return {word: tf_val * idf.get(word, 1.0) for word, tf_val in tf.items()}


def cosine_similarity(vec1: dict, vec2: dict) -> float:
    """Compute cosine similarity between two TF-IDF vectors."""
    if not vec1 or not vec2:
        return 0.0
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    dot = sum(vec1[k] * vec2[k] for k in common)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


# ─── RESUME SCREENING ENGINE ─────────────────────────────────────────────────

def screen_resume(resume_text: str, job: object) -> dict:
    """
    Screen a resume against a job posting.
    Returns score (0-100), feedback, and detailed breakdown.
    """
    job_text = f"{job.title} {job.description} {job.requirements} {job.skills_text}"

    # 1. TF-IDF Cosine Similarity
    vec_resume = compute_tfidf_vector(resume_text)
    vec_job = compute_tfidf_vector(job_text)
    tfidf_score = cosine_similarity(vec_resume, vec_job)

    # 2. Skill Matching
    resume_skills = get_flat_skills(resume_text)
    job_skills = get_flat_skills(job_text)
    # Also parse skills_text directly
    if job.skills_text:
        manual_skills = {s.strip().lower() for s in job.skills_text.split(',') if s.strip()}
        job_skills.update(manual_skills)

    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills
    skill_score = len(matched_skills) / max(len(job_skills), 1)

    # 3. Education match
    resume_edu = extract_education_level(resume_text)
    job_edu_req = extract_education_level(job.requirements + ' ' + job.description)
    edu_weight_resume = EDUCATION_WEIGHTS.get(resume_edu, 0)
    edu_weight_job = EDUCATION_WEIGHTS.get(job_edu_req, 3)  # default bachelor
    edu_score = min(edu_weight_resume / max(edu_weight_job, 1), 1.0)

    # 4. Experience match
    resume_exp = extract_experience_years(resume_text)
    exp_map = {'entry': 1, 'junior': 2, 'mid': 4, 'senior': 6, 'lead': 9}
    required_exp = exp_map.get(job.experience_level, 3)
    exp_score = min(resume_exp / max(required_exp, 1), 1.0)

    # 5. Weighted final score
    final_score = (
        tfidf_score * 35 +
        skill_score * 40 +
        edu_score * 10 +
        exp_score * 15
    )
    final_score = round(min(final_score * 100, 100), 2)

    # 6. Generate feedback
    feedback = _generate_feedback(
        score=final_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_exp=resume_exp,
        required_exp=required_exp,
        resume_edu=resume_edu,
        tfidf_score=tfidf_score
    )

    return {
        'score': final_score,
        'feedback': feedback,
        'details': {
            'tfidf_similarity': round(tfidf_score * 100, 2),
            'skill_match_pct': round(skill_score * 100, 2),
            'matched_skills': sorted(list(matched_skills)),
            'missing_skills': sorted(list(missing_skills))[:10],
            'resume_experience': resume_exp,
            'required_experience': required_exp,
            'resume_education': resume_edu,
            'education_score': round(edu_score * 100, 2),
        }
    }


def _generate_feedback(score, matched_skills, missing_skills, resume_exp,
                        required_exp, resume_edu, tfidf_score):
    """Generate human-readable AI feedback."""
    lines = []

    if score >= 75:
        lines.append("🟢 Strong Match — This resume aligns well with the job requirements.")
    elif score >= 50:
        lines.append("🟡 Moderate Match — Candidate meets several requirements but has some gaps.")
    elif score >= 25:
        lines.append("🟠 Weak Match — Candidate partially meets requirements; significant gaps exist.")
    else:
        lines.append("🔴 Poor Match — Resume does not sufficiently align with this position.")

    if matched_skills:
        lines.append(f"✅ Matched Skills ({len(matched_skills)}): {', '.join(sorted(matched_skills)[:8])}.")
    if missing_skills:
        lines.append(f"❌ Missing Skills: {', '.join(sorted(missing_skills)[:6])}.")

    if resume_exp >= required_exp:
        lines.append(f"✅ Experience: {resume_exp} yrs meets the {required_exp} yr requirement.")
    else:
        lines.append(f"⚠️ Experience gap: Has ~{resume_exp} yrs; role requires ~{required_exp} yrs.")

    if resume_edu != 'unknown':
        lines.append(f"🎓 Education detected: {resume_edu.title()}.")

    return ' '.join(lines)


# ─── JOB RECOMMENDATION ENGINE ───────────────────────────────────────────────

def recommend_jobs(user_resume_text: str, job_postings, top_n: int = 10) -> list:
    """
    Recommend jobs based on resume using TF-IDF + skill matching.
    Returns list of (job, score, reason) tuples sorted by score desc.
    """
    if not user_resume_text or not job_postings:
        return []

    resume_vec = compute_tfidf_vector(user_resume_text)
    resume_skills = get_flat_skills(user_resume_text)
    resume_edu = extract_education_level(user_resume_text)
    resume_exp = extract_experience_years(user_resume_text)

    results = []
    for job in job_postings:
        job_text = f"{job.title} {job.description} {job.requirements} {job.skills_text}"
        job_vec = compute_tfidf_vector(job_text)
        tfidf_sim = cosine_similarity(resume_vec, job_vec)

        job_skills = get_flat_skills(job_text)
        if job.skills_text:
            job_skills.update({s.strip().lower() for s in job.skills_text.split(',') if s.strip()})

        matched = resume_skills & job_skills
        skill_pct = len(matched) / max(len(job_skills), 1)

        exp_map = {'entry': 1, 'junior': 2, 'mid': 4, 'senior': 6, 'lead': 9}
        required_exp = exp_map.get(job.experience_level, 3)
        exp_fit = min(resume_exp / max(required_exp, 1), 1.2)

        score = (tfidf_sim * 40 + skill_pct * 45 + min(exp_fit, 1.0) * 15) * 100
        score = round(min(score, 100), 2)

        reason = _generate_recommendation_reason(
            score, matched, skill_pct, tfidf_sim, resume_exp, required_exp
        )
        results.append((job, score, reason))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


def _generate_recommendation_reason(score, matched_skills, skill_pct, tfidf_sim,
                                     resume_exp, required_exp):
    """Generate recommendation reason text."""
    if score >= 80:
        strength = "Excellent match"
    elif score >= 60:
        strength = "Good match"
    elif score >= 40:
        strength = "Fair match"
    else:
        strength = "Partial match"

    parts = [f"{strength} ({score:.0f}% compatibility)."]
    if matched_skills:
        parts.append(f"Your skills in {', '.join(sorted(matched_skills)[:4])} align with this role.")
    if resume_exp >= required_exp:
        parts.append(f"Your {resume_exp}yr experience fits the requirement.")
    return ' '.join(parts)


# ─── RESUME TEXT EXTRACTION ──────────────────────────────────────────────────

def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract text from uploaded resume file (PDF/DOCX/TXT)."""
    ext = filename.lower().split('.')[-1]
    try:
        if ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif ext == 'pdf':
            return _extract_from_pdf(file_path)
        elif ext in ('doc', 'docx'):
            return _extract_from_docx(file_path)
    except Exception as e:
        return f"[Text extraction failed: {e}]"
    return ''


def _extract_from_pdf(file_path: str) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        return '\n'.join(page.extract_text() or '' for page in reader.pages)
    except ImportError:
        pass
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return '\n'.join(
                page.extract_text() or '' for page in reader.pages
            )
    except Exception as e:
        return f'[PDF extraction error: {e}]'


def _extract_from_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join(para.text for para in doc.paragraphs)
    except Exception as e:
        return f'[DOCX extraction error: {e}]'
