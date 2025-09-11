#!/usr/bin/env python3
"""Flask app with separated templates and static files"""

from flask import Flask, request, jsonify, render_template
import os
import re
import PyPDF2
from collections import defaultdict
import time

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Job roles with detailed descriptions and required skills
job_roles = {
    "software_engineer": {
        "title": "Software Engineer",
        "description": "We are looking for a strong, ambitious developer to join our team. The ideal candidate should be a rockstar programmer with competitive spirit and aggressive problem-solving skills.",
        "required_skills": ["python", "java", "javascript", "software development", "problem solving", "git", "algorithms", "data structures"]
    },
    "senior_software_engineer": {
        "title": "Senior Software Engineer",
        "description": "Seeking a seasoned software engineer with mature leadership skills. The candidate should be experienced in mentoring young developers and have strong technical expertise.",
        "required_skills": ["python", "java", "javascript", "system design", "leadership", "mentoring", "architecture", "code review"]
    },
    "data_scientist": {
        "title": "Data Scientist",
        "description": "Seeking a Data Scientist to analyze complex datasets. The candidate should be energetic and have fresh perspectives on machine learning and statistical analysis.",
        "required_skills": ["python", "machine learning", "data analysis", "statistics", "sql", "data visualization", "pandas", "numpy"]
    },
    "ml_engineer": {
        "title": "Machine Learning Engineer",
        "description": "Looking for an ML Engineer to build and deploy machine learning models. The ideal candidate should be a guru in deep learning and AI technologies.",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "mlops", "docker", "kubernetes"]
    },
    "frontend_developer": {
        "title": "Frontend Developer",
        "description": "Looking for a Frontend Developer with expertise in modern frameworks. The candidate should be a ninja with JavaScript and have strong design skills.",
        "required_skills": ["javascript", "html", "css", "react", "angular", "responsive design", "ui/ux"]
    },
    "backend_developer": {
        "title": "Backend Developer",
        "description": "We need a Backend Developer to build robust server-side applications. The ideal candidate should be experienced and mature in handling complex systems.",
        "required_skills": ["python", "java", "node", "express", "sql", "nosql", "api development", "microservices"]
    },
    "full_stack_developer": {
        "title": "Full Stack Developer",
        "description": "Seeking a versatile full-stack developer who can handle both frontend and backend. The candidate should be aggressive in learning new technologies.",
        "required_skills": ["javascript", "html", "css", "python", "node", "react", "sql", "git", "api development"]
    },
    "devops_engineer": {
        "title": "DevOps Engineer",
        "description": "Looking for a DevOps Engineer to streamline our development processes. The ideal candidate should be a rockstar in automation and cloud technologies.",
        "required_skills": ["docker", "kubernetes", "aws", "ci/cd", "linux", "automation", "terraform", "monitoring"]
    },
    "cloud_architect": {
        "title": "Cloud Architect",
        "description": "We need a Cloud Architect to design our cloud infrastructure. The candidate should be experienced and have strong knowledge of cloud platforms.",
        "required_skills": ["aws", "azure", "gcp", "terraform", "cloud security", "microservices", "system design", "cost optimization"]
    },
    "product_manager": {
        "title": "Product Manager",
        "description": "Seeking a Product Manager to lead our product development. The ideal candidate should be aggressive in market research and competitive in strategy.",
        "required_skills": ["product management", "agile", "user stories", "market research", "roadmapping", "stakeholder management"]
    }
}

# Bias detection keywords
BIAS_KEYWORDS = {
    "gender": {
        "male_biased": ["strong", "aggressive", "competitive", "dominant", "assertive"],
        "female_biased": ["nurturing", "collaborative", "supportive"],
        "neutral": ["skilled", "qualified", "experienced", "proficient"]
    },
    "age": {
        "biased": ["young", "energetic", "fresh", "recent graduate", "digital native", "mature", "experienced", "seasoned"],
        "neutral": ["qualified", "skilled", "talented"]
    },
    "personality": {
        "biased": ["rockstar", "ninja", "guru", "fast-paced"],
        "neutral": ["motivated", "dedicated", "team-oriented"]
    }
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        print(f"Attempting to extract text from: {file_path}")
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            print(f"PDF has {len(reader.pages)} pages")
            
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        print(f"Extracted {len(page_text)} characters from page {i+1}")
                except Exception as e:
                    print(f"Error extracting page {i+1}: {str(e)}")
                    continue
            
            if not text.strip():
                return "Error: Could not extract text from PDF. The PDF might be image-based or encrypted."
            
            print(f"Total extracted text length: {len(text)}")
            return text
            
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return f"Error extracting PDF: {str(e)}"

def anonymize_resume(text):
    """Remove personal identifiers from resume"""
    # Replace names
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[CANDIDATE NAME]', text)
    # Replace emails
    text = re.sub(r'\b\w+@\w+\.\w+\b', '[EMAIL]', text)
    # Replace phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    # Replace gender indicators
    text = re.sub(r'\b(Male|Female|man|woman|he/him|she/her)\b', '[GENDER]', text, flags=re.IGNORECASE)
    return text

def analyze_job_description_bias(text):
    """Detect biased language in job descriptions"""
    words = text.lower().split()
    bias_report = defaultdict(list)
    
    for category, bias_types in BIAS_KEYWORDS.items():
        for bias_type, keywords in bias_types.items():
            if bias_type != "neutral":
                for word in words:
                    if word in keywords:
                        bias_report[category].append(word)
    
    return bias_report

def extract_skills_from_text(text):
    """Extract skills from resume text"""
    common_skills = [
        "python", "java", "javascript", "html", "css", "sql", "nosql", "mongodb",
        "react", "angular", "vue", "node", "express", "django", "flask",
        "machine learning", "data analysis", "data science", "ai", "artificial intelligence",
        "git", "docker", "kubernetes", "aws", "azure", "gcp",
        "project management", "agile", "scrum", "leadership", "teamwork",
        "algorithms", "data structures", "pandas", "numpy", "tensorflow", "pytorch"
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

def calculate_job_match(resume_skills, job_skills):
    """Calculate how well resume matches job requirements"""
    if not job_skills:
        return 0
    
    matching_skills = list(set(resume_skills) & set(job_skills))
    match_percentage = (len(matching_skills) / len(job_skills)) * 100
    
    return {
        "match_percentage": round(match_percentage, 2),
        "matching_skills": matching_skills,
        "missing_skills": list(set(job_skills) - set(resume_skills))
    }

def generate_confusion_matrix():
    """Generate confusion matrix data for bias detection"""
    test_data = [
        ("We need a strong, aggressive programmer who is a rockstar at coding", True),
        ("Looking for a young, energetic developer with fresh ideas", True),
        ("Seeking a competitive ninja who can dominate the market", True),
        ("We want a guru in machine learning with assertive leadership", True),
        ("Need an experienced, mature developer for senior role", True),
        ("We need a skilled programmer with problem-solving abilities", False),
        ("Looking for a qualified developer with technical expertise", False),
        ("Seeking a proficient candidate with relevant experience", False),
        ("We want a talented professional with good communication skills", False),
        ("Need a dedicated developer for software development role", False),
        ("Experienced professional with strong technical skills", True),
        ("Collaborative team player with good communication", False),
        ("Seasoned developer with mature approach to problems", True),
        ("Qualified candidate with proven track record", False),
        ("Energetic team member with fresh perspectives", True),
    ]
    
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    results = []
    
    for description, true_label in test_data:
        predicted_bias = len(analyze_job_description_bias(description)) > 0
        
        if predicted_bias and true_label:
            true_positive += 1
            status = "correct"
        elif not predicted_bias and not true_label:
            true_negative += 1
            status = "correct"
        elif predicted_bias and not true_label:
            false_positive += 1
            status = "incorrect"
        else:
            false_negative += 1
            status = "incorrect"
        
        results.append({
            'description': description,
            'predicted': 'Biased' if predicted_bias else 'Clean',
            'actual': 'Biased' if true_label else 'Clean',
            'status': status
        })
    
    total = len(test_data)
    accuracy = (true_positive + true_negative) / total
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'matrix': {
            'true_positive': true_positive,
            'true_negative': true_negative,
            'false_positive': false_positive,
            'false_negative': false_negative
        },
        'metrics': {
            'accuracy': round(accuracy, 3),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1_score, 3)
        },
        'results': results
    }

@app.route('/')
def index():
    return render_template('index.html', job_roles=job_roles)

@app.route('/confusion-matrix')
def confusion_matrix():
    """Display confusion matrix page"""
    matrix_data = generate_confusion_matrix()
    return render_template('confusion_matrix.html', matrix_data=matrix_data)

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        print("Upload request received")
        
        if 'resume' not in request.files:
            print("No resume file in request")
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['resume']
        job_role = request.form.get('job_role')
        
        print(f"File: {file.filename}, Job role: {job_role}")
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if not job_role:
            return jsonify({'error': 'No job role selected'})
        
        if not job_role in job_roles:
            return jsonify({'error': 'Invalid job role selected'})
        
        if file and file.filename.lower().endswith('.pdf'):
            # Create uploads directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save the uploaded file with a safe filename
            safe_filename = f"resume_{int(time.time())}_{file.filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            
            print(f"Saving file to: {file_path}")
            file.save(file_path)
            
            # Verify file was saved
            if not os.path.exists(file_path):
                return jsonify({'error': 'Failed to save uploaded file'})
            
            print(f"File saved successfully, size: {os.path.getsize(file_path)} bytes")
            
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file_path)
            
            print(f"Extracted text length: {len(resume_text)}")
            
            if "Error extracting PDF" in resume_text or "Error:" in resume_text:
                # Clean up the file
                try:
                    os.remove(file_path)
                except:
                    pass
                return jsonify({'error': resume_text})
            
            # Anonymize resume
            anonymized_resume = anonymize_resume(resume_text)
            
            # Get job details
            job_data = job_roles[job_role]
            job_description = job_data['description']
            required_skills = job_data['required_skills']
            
            # Extract skills from resume
            resume_skills = extract_skills_from_text(resume_text)
            
            # Calculate job match
            match_result = calculate_job_match(resume_skills, required_skills)
            
            # Analyze job description for bias
            bias_report = analyze_job_description_bias(job_description)
            
            # Format bias details
            bias_details = []
            bias_detected = False
            for category, words in bias_report.items():
                if words:
                    bias_detected = True
                    bias_details.append({
                        'category': category.title(),
                        'words': list(set(words))
                    })
            
            # Generate recommendation
            match_percentage = match_result['match_percentage']
            if match_percentage >= 70:
                recommendation = "Excellent match! This candidate meets most job requirements."
            elif match_percentage >= 40:
                recommendation = "Good match with some skill gaps that could be addressed through training."
            else:
                recommendation = "Limited match. Consider if the candidate has transferable skills or potential for growth."
            
            # Clean up the uploaded file after processing
            try:
                os.remove(file_path)
            except:
                pass
            
            print("Analysis completed successfully")
            
            return jsonify({
                'match_percentage': match_percentage,
                'matching_skills': match_result['matching_skills'],
                'missing_skills': match_result['missing_skills'],
                'recommendation': recommendation,
                'bias_detected': bias_detected,
                'bias_details': bias_details,
                'anonymized_resume': anonymized_resume,
                'job_title': job_data['title']
            })
        
        return jsonify({'error': 'Please upload a PDF file'})
        
    except Exception as e:
        print(f"Server error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=False, host='0.0.0.0', port=port)