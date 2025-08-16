import os
import pandas as pd
import re
import nltk
import json
from nltk.tokenize import word_tokenize
from collections import defaultdict
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import filedialog, messagebox

# Import PDF handling functionality
from pdf_handler import extract_text_from_pdf, select_pdf_file, batch_process_pdfs

# Import job roles
from job_roles import job_roles

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')

# Use simpler tokenizer to avoid punkt_tab dependency
def custom_tokenize(text):
    """Simple tokenizer that splits on whitespace and punctuation"""
    # Remove punctuation and split on whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().split()

# Comprehensive bias keywords (customize as needed)
BIAS_KEYWORDS = {
    "gender": {
        "male_biased": ["he", "him", "his", "man", "men", "gentleman", "boys", "salesman", "chairman", "businessman", "manpower", "manmade"],
        "female_biased": ["she", "her", "hers", "woman", "women", "lady", "ladies", "girls", "saleswoman", "chairwoman", "businesswoman"],
        "neutral": ["they", "them", "their", "person", "people", "individual", "candidate", "applicant"]
    },
    "ethnicity": {
        "biased": ["native", "foreign", "immigrant", "minority", "exotic", "ghetto", "urban", "diverse"],
        "neutral": ["all backgrounds", "all nationalities", "multicultural"]
    },
    "age": {
        "biased": ["young", "energetic", "fresh", "recent graduate", "digital native", "mature", "experienced", "seasoned", "veteran"],
        "neutral": ["qualified", "skilled", "talented", "proficient"]
    },
    "personality": {
        "biased": ["aggressive", "ambitious", "competitive", "rockstar", "ninja", "guru", "strong", "fast-paced", "dominant", "assertive"],
        "neutral": ["motivated", "dedicated", "collaborative", "team-oriented", "skilled", "proficient"]
    },
    "education": {
        "biased": ["ivy league", "top-tier", "elite", "prestigious", "world-class"],
        "neutral": ["qualified", "educated", "trained", "knowledgeable"]
    }
}

# Personal identifiers to anonymize
PERSONAL_IDENTIFIERS = [
    r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Names (simple pattern)
    r'\b[A-Z][a-z]+\b',  # First names
    r'\b\w+@\w+\.\w+\b',  # Email addresses
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone numbers
    r'\b(Male|Female|man|woman|he/him|she/her)\b',  # Gender indicators
    r'\b(Black|White|Asian|Hispanic|Latino|African American|Caucasian)\b',  # Ethnicity indicators
    r'\b(University of|College|School)\s[A-Za-z\s]+\b',  # University names
]

def analyze_job_description(text):
    """Detect biased words in job descriptions"""
    words = custom_tokenize(text)
    bias_report = defaultdict(lambda: defaultdict(list))
    
    for bias_category, bias_types in BIAS_KEYWORDS.items():
        for bias_type, keywords in bias_types.items():
            for word in words:
                if word in keywords:
                    bias_report[bias_category][bias_type].append(word)
    
    return bias_report

def generate_suggestions(bias_report):
    """Suggest neutral alternatives for biased language"""
    suggestions = []
    
    for category, bias_types in bias_report.items():
        if category == "gender":
            if bias_types["male_biased"]:
                suggestions.append(f"🔴 Male-biased words detected: {', '.join(set(bias_types['male_biased']))}")
                suggestions.append(f"✅ Try neutral alternatives: {', '.join(BIAS_KEYWORDS['gender']['neutral'])}")
            
            if bias_types["female_biased"]:
                suggestions.append(f"🔴 Female-biased words detected: {', '.join(set(bias_types['female_biased']))}")
                suggestions.append(f"✅ Try neutral alternatives: {', '.join(BIAS_KEYWORDS['gender']['neutral'])}")
        else:
            if bias_types["biased"]:
                suggestions.append(f"🔴 {category.capitalize()}-biased words detected: {', '.join(set(bias_types['biased']))}")
                suggestions.append(f"✅ Try neutral alternatives: {', '.join(BIAS_KEYWORDS[category]['neutral'])}")
    
    return suggestions if suggestions else ["🟢 No strong bias detected"]

def anonymize_resume(text):
    """Anonymize personal identifiers in resumes"""
    anonymized_text = text
    
    # Replace personal identifiers with generic placeholders
    for i, pattern in enumerate(PERSONAL_IDENTIFIERS):
        if i == 0:  # Full names
            anonymized_text = re.sub(pattern, "[CANDIDATE NAME]", anonymized_text)
        elif i == 1:  # First names
            # Skip if we've already replaced full names
            continue
        elif i == 2:  # Email
            anonymized_text = re.sub(pattern, "[EMAIL]", anonymized_text)
        elif i == 3:  # Phone
            anonymized_text = re.sub(pattern, "[PHONE]", anonymized_text)
        elif i == 4:  # Gender
            anonymized_text = re.sub(pattern, "[GENDER]", anonymized_text)
        elif i == 5:  # Ethnicity
            anonymized_text = re.sub(pattern, "[ETHNICITY]", anonymized_text)
        elif i == 6:  # University
            anonymized_text = re.sub(pattern, "[UNIVERSITY]", anonymized_text)
    
    return anonymized_text

def extract_skills(text):
    """Extract skills from resume text"""
    # This is a simple implementation - in a real system, you would use a more sophisticated
    # approach with a comprehensive skills database or ML model
    common_skills = [
        "python", "java", "javascript", "html", "css", "sql", "nosql", "mongodb", 
        "react", "angular", "vue", "node", "express", "django", "flask", 
        "machine learning", "data analysis", "data science", "ai", "artificial intelligence",
        "nlp", "natural language processing", "computer vision", "deep learning",
        "project management", "agile", "scrum", "kanban", "leadership", "teamwork",
        "communication", "problem solving", "critical thinking", "creativity"
    ]
    
    skills_found = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            skills_found.append(skill)
    
    return skills_found

def calculate_job_match(resume_text, job_description):
    """Calculate match between resume and job description based on skills"""
    # Extract skills from both documents
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    # Calculate TF-IDF vectors for more sophisticated matching
    try:
        stop_words = set(stopwords.words('english'))
    except:
        # Fallback if stopwords not available
        stop_words = set(['a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                         'when', 'where', 'how', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                         'have', 'has', 'had', 'do', 'does', 'did', 'to', 'at', 'by', 'for', 'with',
                         'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
                         'above', 'below', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under'])
    
    # Use a simple approach if TF-IDF fails
    try:
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        
        # Create a small corpus with just these two documents
        corpus = [resume_text, job_description]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        # Fallback to a simpler similarity calculation
        resume_words = set(custom_tokenize(resume_text))
        job_words = set(custom_tokenize(job_description))
        
        if len(job_words) > 0:
            similarity = len(resume_words.intersection(job_words)) / len(job_words)
        else:
            similarity = 0
    
    # Calculate skill match percentage
    if job_skills:
        skill_match = len(set(resume_skills).intersection(set(job_skills))) / len(job_skills)
    else:
        skill_match = 0
    
    return {
        "semantic_similarity": similarity,
        "skill_match_percentage": skill_match * 100,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": list(set(resume_skills).intersection(set(job_skills)))
    }

def evaluate_candidate(resume_text, job_description):
    """Evaluate a candidate based on skills and experience, not personal attributes"""
    # Step 1: Anonymize the resume
    anonymized_resume = anonymize_resume(resume_text)
    
    # Step 2: Calculate job match
    match_results = calculate_job_match(anonymized_resume, job_description)
    
    # Step 3: Check for bias in job description
    bias_report = analyze_job_description(job_description)
    bias_suggestions = generate_suggestions(bias_report)
    
    return {
        "anonymized_resume": anonymized_resume,
        "match_results": match_results,
        "bias_analysis": {
            "report": bias_report,
            "suggestions": bias_suggestions
        }
    }

def load_job_descriptions():
    """Load job descriptions from job_roles module"""
    job_descriptions = {}
    
    for job_id, job_data in job_roles.items():
        job_descriptions[job_id] = f"{job_data['title']}\n\n{job_data['description']}\n\nRequired Skills: {', '.join(job_data['required_skills'])}"
    
    return job_descriptions

def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 50)
    print("🤖 AI for Detecting and Reducing Bias in Hiring")
    print("=" * 50)
    print("1. Analyze Job Role for Bias")
    print("2. Anonymize PDF Resume")
    print("3. Evaluate PDF Resume for Job Role")
    print("4. Batch Process PDF Resumes")
    print("5. Exit")
    print("=" * 50)
    
    return input("Enter your choice (1-5): ")

def load_resume(file_path=None):
    """Load resume from PDF file or select one via dialog"""
    # If no file path provided, open file selection dialog
    if not file_path:
        pdf_path, extracted_text = select_pdf_file()
        if pdf_path and extracted_text:
            return extracted_text
        else:
            # If user canceled or error occurred, use a sample PDF
            sample_dir = os.path.join(os.path.dirname(__file__), "sample_pdfs")
            if os.path.exists(sample_dir):
                sample_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
                if sample_files:
                    sample_path = os.path.join(sample_dir, sample_files[0])
                    return extract_text_from_pdf(sample_path)
            
            # Fallback if no sample PDFs found
            print("No PDF selected and no sample PDFs found. Using default text.")
            return """Sarah Johnson
Email: sarah.johnson@email.com
Phone: 555-987-6543
Gender: Female

Education:
Stanford University - Master's in Computer Science

Skills:
Python, Java, JavaScript, HTML/CSS, SQL, React, Node.js, Machine Learning

Experience:
- Senior Developer at Tech Innovations Inc. (2019-Present)
  Led development of machine learning algorithms for customer segmentation
  Managed a team of 4 junior developers on various projects

- Web Developer at Digital Solutions LLC (2016-2019)
  Developed responsive web applications using React and Node.js
  Collaborated with UX designers to implement user-friendly interfaces"""
    
    # If file path is provided, extract text from it
    if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        print(f"Invalid PDF file path: {file_path}")
        return None

def visualize_bias_report(bias_report):
    """Create a simple visualization of bias categories"""
    bias_counts = {}
    
    for category, bias_types in bias_report.items():
        total_biased = 0
        for bias_type, words in bias_types.items():
            if bias_type != "neutral":
                total_biased += len(set(words))
        
        if total_biased > 0:
            bias_counts[category] = total_biased
    
    if bias_counts:
        print("\n📊 Bias Distribution:")
        for category, count in bias_counts.items():
            bar = "█" * min(count, 20)  # Limit bar length
            print(f"{category.capitalize()}: {bar} ({count})")
    else:
        print("\n📊 No bias detected in any category.")

def analyze_job_description_menu():
    """Menu option for analyzing job roles"""
    print("\n📋 Available Job Roles:")
    job_descriptions = load_job_descriptions()
    
    # Display available job roles
    for i, (job_id, job_text) in enumerate(job_descriptions.items(), 1):
        job_title = job_roles[job_id]['title']
        print(f"{i}. {job_title}")
    
    choice = input("\nSelect a job role (number): ")
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(job_descriptions):
            job_id = list(job_descriptions.keys())[index]
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
        else:
            print("Invalid selection. Using first job role.")
            job_id = list(job_descriptions.keys())[0]
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
    except (ValueError, IndexError):
        print("Invalid selection. Using first job role.")
        job_id = list(job_descriptions.keys())[0]
        job_text = job_descriptions[job_id]
        job_title = job_roles[job_id]['title']
    
    print(f"\n🔎 Analyzing Job Role: {job_title}")
    print(job_text)
    
    # Analyze job description for bias
    bias_report = analyze_job_description(job_text)
    bias_suggestions = generate_suggestions(bias_report)
    
    print("\n📝 Bias Report:")
    for suggestion in bias_suggestions:
        print("- " + suggestion)
    
    # Visualize bias distribution
    visualize_bias_report(bias_report)
    
    return job_text, bias_report, job_id

def anonymize_resume_menu():
    """Menu option for anonymizing PDF resumes"""
    print("\n📄 Resume Source Options:")
    print("1. Use sample PDF resume")
    print("2. Upload PDF file")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        # Use a sample PDF from the sample_pdfs directory
        sample_dir = os.path.join(os.path.dirname(__file__), "sample_pdfs")
        if os.path.exists(sample_dir):
            sample_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
            if sample_files:
                sample_path = os.path.join(sample_dir, sample_files[0])
                resume_text = extract_text_from_pdf(sample_path)
                print(f"Using sample PDF: {sample_files[0]}")
            else:
                resume_text = load_resume()
        else:
            resume_text = load_resume()
    elif choice == "2":
        # Open file dialog to select PDF
        resume_text = load_resume()
    else:
        print("Invalid option. Using sample resume.")
        resume_text = load_resume()
    
    print("\n📄 Original Resume:")
    print(resume_text)
    
    print("\n🔒 Anonymized Resume:")
    anonymized_resume = anonymize_resume(resume_text)
    print(anonymized_resume)
    
    save_option = input("\nSave anonymized resume? (y/n): ")
    if save_option.lower() == 'y':
        filename = input("Enter filename to save: ")
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(anonymized_resume)
        
        print(f"Anonymized resume saved as {filename}")
    
    return resume_text, anonymized_resume

def evaluate_candidate_menu():
    """Menu option for evaluating candidates against job roles"""
    # First select job role
    print("\n📋 Available Job Roles:")
    job_descriptions = load_job_descriptions()
    
    # Display available job roles
    for i, (job_id, _) in enumerate(job_descriptions.items(), 1):
        job_title = job_roles[job_id]['title']
        print(f"{i}. {job_title}")
    
    try:
        choice = int(input("\nSelect a job role (number): ")) - 1
        if 0 <= choice < len(job_descriptions):
            job_id = list(job_descriptions.keys())[choice]
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
        else:
            print("Invalid selection. Using first job role.")
            job_id = list(job_descriptions.keys())[0]
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
    except (ValueError, IndexError):
        print("Invalid selection. Using first job role.")
        job_id = list(job_descriptions.keys())[0]
        job_text = job_descriptions[job_id]
        job_title = job_roles[job_id]['title']
    
    print(f"\n🔎 Selected Job Role: {job_title}")
    print(job_text)
    
    # Now load resume from PDF
    print("\n📄 Resume Source Options:")
    print("1. Use sample PDF resume")
    print("2. Upload PDF file")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        # Use a sample PDF from the sample_pdfs directory
        sample_dir = os.path.join(os.path.dirname(__file__), "sample_pdfs")
        if os.path.exists(sample_dir):
            sample_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
            if sample_files:
                sample_path = os.path.join(sample_dir, sample_files[0])
                resume_text = extract_text_from_pdf(sample_path)
                print(f"Using sample PDF: {sample_files[0]}")
            else:
                resume_text = load_resume()
        else:
            resume_text = load_resume()
    elif choice == "2":
        # Open file dialog to select PDF
        resume_text = load_resume()
        if not resume_text:  # If PDF extraction failed or was canceled
            print("Using sample resume instead.")
            resume_text = load_resume()
    else:
        print("Invalid choice. Using sample resume.")
        resume_text = load_resume()
    
    print("\n📄 Resume:")
    print(resume_text)
    
    print("\n🔒 Anonymized Resume:")
    anonymized_resume = anonymize_resume(resume_text)
    print(anonymized_resume)
    
    print("\n🧩 Candidate Evaluation:")
    evaluation = evaluate_candidate(resume_text, job_text)
    
    print(f"Semantic Similarity: {evaluation['match_results']['semantic_similarity']:.2f}")
    print(f"Skill Match: {evaluation['match_results']['skill_match_percentage']:.2f}%")
    print(f"Skills Found: {', '.join(evaluation['match_results']['resume_skills'])}")
    print(f"Matching Skills: {', '.join(evaluation['match_results']['matching_skills'])}")
    
    # Bias analysis of job description
    print("\n📝 Job Role Bias Analysis:")
    for suggestion in evaluation['bias_analysis']['suggestions']:
        print("- " + suggestion)
    
    # Visualize bias distribution
    visualize_bias_report(evaluation['bias_analysis']['report'])
    
    return evaluation

def batch_process_resumes():
    """Process multiple resumes against a job description"""
    # First select job role option
    print("\n📋 Job Role Options:")
    print("1. Select a specific job role")
    print("2. Evaluate against 5 random job roles")
    
    choice = input("\nSelect option: ")
    
    job_descriptions = load_job_descriptions()
    
    if choice == "1":
        # Display available job roles
        print("\n📋 Available Job Roles:")
        for i, (job_id, _) in enumerate(job_descriptions.items(), 1):
            job_title = job_roles[job_id]['title']
            print(f"{i}. {job_title}")
        
        try:
            choice = int(input("\nSelect a job role (number): ")) - 1
            if 0 <= choice < len(job_descriptions):
                job_id = list(job_descriptions.keys())[choice]
                job_text = job_descriptions[job_id]
                job_title = job_roles[job_id]['title']
            else:
                print("Invalid selection. Using first job role.")
                job_id = list(job_descriptions.keys())[0]
                job_text = job_descriptions[job_id]
                job_title = job_roles[job_id]['title']
        except (ValueError, IndexError):
            print("Invalid selection. Using first job role.")
            job_id = list(job_descriptions.keys())[0]
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
        
        print(f"\n🔎 Selected Job Role: {job_title}")
        print(job_text)
        
        print("\nSelect a directory containing PDF resumes to process...")
        results = batch_process_pdfs(job_text)
        
        if not results:
            print("No results to display. Batch processing was canceled or no PDFs were found.")
            return
        
        # Sort results by skill match percentage
        sorted_results = sorted(results, key=lambda x: x['evaluation']['match_results']['skill_match_percentage'], reverse=True)
        
        print(f"\n📊 Batch Processing Results for {job_title} (Ranked by Skill Match):")
        print("-" * 80)
        
        for i, result in enumerate(sorted_results, 1):
            eval_data = result['evaluation']
            print(f"Rank #{i}: {result['filename']}")
            print(f"Skill Match: {eval_data['match_results']['skill_match_percentage']:.2f}%")
            print(f"Semantic Similarity: {eval_data['match_results']['semantic_similarity']:.2f}")
            print(f"Matching Skills: {', '.join(eval_data['match_results']['matching_skills'])}")
            print("-" * 80)
        
        return sorted_results
    
    elif choice == "2":
        # Select 5 random job roles
        import random
        job_ids = list(job_descriptions.keys())
        random_job_ids = random.sample(job_ids, min(5, len(job_ids)))
        
        print("\nSelect a PDF resume to evaluate against multiple job roles...")
        resume_text = load_resume()
        
        if not resume_text:
            print("No resume selected. Operation canceled.")
            return
        
        print("\n📊 Evaluating Resume Against Multiple Job Roles:")
        print("-" * 80)
        
        all_results = []
        
        for job_id in random_job_ids:
            job_text = job_descriptions[job_id]
            job_title = job_roles[job_id]['title']
            
            print(f"\n🔎 Evaluating for: {job_title}")
            
            evaluation = evaluate_candidate(resume_text, job_text)
            
            match_percentage = evaluation['match_results']['skill_match_percentage']
            similarity = evaluation['match_results']['semantic_similarity']
            matching_skills = evaluation['match_results']['matching_skills']
            
            print(f"Skill Match: {match_percentage:.2f}%")
            print(f"Semantic Similarity: {similarity:.2f}")
            print(f"Matching Skills: {', '.join(matching_skills)}")
            print("-" * 80)
            
            all_results.append({
                'job_title': job_title,
                'job_id': job_id,
                'evaluation': evaluation
            })
        
        # Sort results by skill match percentage
        sorted_results = sorted(all_results, key=lambda x: x['evaluation']['match_results']['skill_match_percentage'], reverse=True)
        
        print("\n📊 Summary of Results (Best Job Role Matches):")
        print("-" * 80)
        
        for i, result in enumerate(sorted_results, 1):
            eval_data = result['evaluation']
            print(f"Rank #{i}: {result['job_title']}")
            print(f"Skill Match: {eval_data['match_results']['skill_match_percentage']:.2f}%")
            print(f"Semantic Similarity: {eval_data['match_results']['semantic_similarity']:.2f}")
            print("-" * 80)
        
        return sorted_results
    
    else:
        print("Invalid choice. Operation canceled.")
        return None

# Main program
if __name__ == "__main__":
    while True:
        choice = display_menu()
        
        if choice == '1':
            analyze_job_description_menu()
        elif choice == '2':
            anonymize_resume_menu()
        elif choice == '3':
            evaluate_candidate_menu()
        elif choice == '4':
            batch_process_resumes()
        elif choice == '5':
            print("\nThank you for using the AI Bias Detection and Reduction System!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")