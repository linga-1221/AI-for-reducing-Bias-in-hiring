from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from src.processing.pdf_handler import extract_text_from_pdf
#from pdf_handler import extract_text_from_pdf
from main import anonymize_resume, analyze_job_description, generate_suggestions
from job_roles import job_roles

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html', job_roles=job_roles)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and file.filename.endswith('.pdf'):
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)
        
        # Anonymize resume
        anonymized_resume = anonymize_resume(resume_text)
        
        # Get selected job role
        job_id = request.form.get('job_role')
        job_description = job_roles[job_id]['description']
        required_skills = job_roles[job_id]['required_skills']
        
        # Analyze bias in job description
        bias_report = analyze_job_description(job_description)
        bias_suggestions = generate_suggestions(bias_report)
        
        # Check if there's any real bias or just false positives
        has_real_bias = False
        for category, bias_types in bias_report.items():
            for bias_type, words in bias_types.items():
                if words and bias_type != "neutral":
                    # Filter out common false positives
                    filtered_words = [w for w in words if not (w == "strong" and category == "personality")]
                    if filtered_words:
                        has_real_bias = True
        
        # If no real bias is detected, override suggestions
        if not has_real_bias:
            bias_suggestions = ["🟢 No significant bias detected in this job description."]
        
        # Format required skills for better presentation
        formatted_skills = []
        for skill in required_skills:
            formatted_skills.append(f"✅ {skill.title()}")
        
        return jsonify({
            'resume_text': resume_text,
            'anonymized_resume': anonymized_resume,
            'bias_analysis': {
                'report': bias_report,
                'suggestions': bias_suggestions
            },
            'required_skills': formatted_skills
        })
    
    return jsonify({'error': 'Invalid file format. Please upload a PDF file.'})

@app.route('/templates/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True)