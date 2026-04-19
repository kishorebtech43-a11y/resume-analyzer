from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    skills_list = [
    # Programming
    "python", "java", "javascript", "c", "c++",

    # Web
    "html", "css", "react", "node", "flask", "django",

    # Database
    "sql", "mongodb",

    # Tools
    "git", "github", "linux",

    # IT / Helpdesk (VERY IMPORTANT for your resume)
    "troubleshooting", "networking", "technical support",
    "helpdesk", "windows", "hardware", "software",
    "customer support", "ticketing", "system support"
]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if re.search(r'\b' + skill + r'\b', text):
            found_skills.append(skill)

    return found_skills


@app.route('/analyze', methods=['POST'])
def analyze():
    resume = request.files['resume']
    job_desc = request.form['job_desc']

    resume_text = extract_text(resume)

    # Similarity
    text = [resume_text, job_desc]
    cv = CountVectorizer().fit_transform(text)
    similarity = cosine_similarity(cv)[0][1]

    # ✅ STEP 1: Calculate score OUTSIDE return
    score = round(similarity * 100, 2)

    if score > 80:
        rating = "Excellent"
    elif score > 60:
        rating = "Good"
    elif score > 40:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    # Skill extraction
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    # ✅ STEP 2: RETURN dictionary only
    return jsonify({
        "match_percentage": score,
        "rating": rating,
        "matched_skills": matched,
        "missing_skills": missing
    })
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)