#!/usr/bin/env bash
# TalentAI — One-command setup
set -e

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   TalentAI — Setup & Launch          ║"
echo "╚══════════════════════════════════════╝"
echo ""

# 1. Virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate  (works on Linux/Mac and Git Bash on Windows)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 3. Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 4. Media directories
mkdir -p media/resumes media/avatars media/company_logos

# 5. Migrations
echo "🗄️  Running migrations..."
python manage.py makemigrations core --no-input
python manage.py migrate --no-input

# 6. Seed demo data
echo "🌱 Seeding demo data..."
python manage.py seed_demo

echo ""
echo "✅ Setup complete!"
echo ""
echo "   Start the server:"
echo "   source venv/bin/activate && python manage.py runserver"
echo ""
echo "   Open → http://127.0.0.1:8000/"
echo ""
