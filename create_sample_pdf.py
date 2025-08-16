from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_sample_resume():
    """Create a sample PDF resume for testing"""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_pdfs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the output path
    output_path = os.path.join(output_dir, "sample_resume.pdf")
    
    # Create the PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6
    )
    
    normal_style = styles["Normal"]
    
    # Build the content
    content = []
    
    # Personal Information
    content.append(Paragraph("John Smith", title_style))
    content.append(Paragraph("Email: john.smith@email.com | Phone: 555-123-4567 | Gender: Male", normal_style))
    content.append(Spacer(1, 12))
    
    # Education
    content.append(Paragraph("Education", heading_style))
    content.append(Paragraph("Harvard University - Master's in Computer Science (2015-2017)", normal_style))
    content.append(Paragraph("University of California - Bachelor's in Computer Engineering (2011-2015)", normal_style))
    content.append(Spacer(1, 12))
    
    # Skills
    content.append(Paragraph("Skills", heading_style))
    skills_text = "Python, Java, C++, JavaScript, React, Node.js, SQL, MongoDB, Docker, Kubernetes, "
    skills_text += "Machine Learning, Data Analysis, Cloud Computing (AWS, Azure), Git, CI/CD"
    content.append(Paragraph(skills_text, normal_style))
    content.append(Spacer(1, 12))
    
    # Experience
    content.append(Paragraph("Experience", heading_style))
    
    # Experience 1
    content.append(Paragraph("<b>Senior Software Engineer at Tech Solutions Inc. (2019-Present)</b>", normal_style))
    exp1 = [
        "Led development of a machine learning platform that increased customer retention by 25%",
        "Managed a team of 5 developers working on cloud-based applications",
        "Implemented CI/CD pipelines that reduced deployment time by 40%",
        "Designed and developed RESTful APIs for mobile and web applications"
    ]
    for item in exp1:
        content.append(Paragraph(f"• {item}", normal_style))
    content.append(Spacer(1, 6))
    
    # Experience 2
    content.append(Paragraph("<b>Software Developer at DataTech Corp. (2017-2019)</b>", normal_style))
    exp2 = [
        "Developed data processing pipelines using Python and Apache Spark",
        "Created interactive dashboards using React and D3.js",
        "Optimized database queries that improved application performance by 30%",
        "Collaborated with UX designers to implement user-friendly interfaces"
    ]
    for item in exp2:
        content.append(Paragraph(f"• {item}", normal_style))
    
    # Build the PDF
    doc.build(content)
    
    print(f"Sample resume PDF created at: {output_path}")
    return output_path

def create_multiple_sample_resumes(count=3):
    """Create multiple sample PDF resumes with variations"""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_pdfs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample candidate data
    candidates = [
        {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "555-123-4567",
            "gender": "Male",
            "education": [
                "Harvard University - Master's in Computer Science (2015-2017)",
                "University of California - Bachelor's in Computer Engineering (2011-2015)"
            ],
            "skills": "Python, Java, C++, JavaScript, React, Node.js, SQL, MongoDB, Docker, Kubernetes, Machine Learning",
            "experience": [
                {
                    "title": "Senior Software Engineer at Tech Solutions Inc. (2019-Present)",
                    "details": [
                        "Led development of a machine learning platform that increased customer retention by 25%",
                        "Managed a team of 5 developers working on cloud-based applications",
                        "Implemented CI/CD pipelines that reduced deployment time by 40%"
                    ]
                },
                {
                    "title": "Software Developer at DataTech Corp. (2017-2019)",
                    "details": [
                        "Developed data processing pipelines using Python and Apache Spark",
                        "Created interactive dashboards using React and D3.js",
                        "Optimized database queries that improved application performance by 30%"
                    ]
                }
            ]
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "555-987-6543",
            "gender": "Female",
            "education": [
                "Stanford University - Master's in Computer Science (2016-2018)",
                "MIT - Bachelor's in Electrical Engineering (2012-2016)"
            ],
            "skills": "Python, Java, JavaScript, HTML/CSS, SQL, React, Node.js, Machine Learning, Data Analysis, AWS",
            "experience": [
                {
                    "title": "Senior Developer at Tech Innovations Inc. (2019-Present)",
                    "details": [
                        "Led development of machine learning algorithms for customer segmentation",
                        "Managed a team of 4 junior developers on various projects",
                        "Implemented cloud-based solutions using AWS services"
                    ]
                },
                {
                    "title": "Web Developer at Digital Solutions LLC (2016-2019)",
                    "details": [
                        "Developed responsive web applications using React and Node.js",
                        "Collaborated with UX designers to implement user-friendly interfaces",
                        "Maintained and optimized database performance"
                    ]
                }
            ]
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@email.com",
            "phone": "555-456-7890",
            "gender": "Male",
            "education": [
                "UC Berkeley - Ph.D. in Computer Science (2014-2018)",
                "University of Washington - Bachelor's in Computer Science (2010-2014)"
            ],
            "skills": "Python, TensorFlow, PyTorch, Deep Learning, NLP, Computer Vision, Data Science, R, SQL, Cloud Computing",
            "experience": [
                {
                    "title": "AI Research Scientist at AI Innovations (2018-Present)",
                    "details": [
                        "Developed novel deep learning models for natural language processing",
                        "Published 3 papers in top-tier AI conferences",
                        "Created a computer vision system that improved accuracy by 15%"
                    ]
                },
                {
                    "title": "Data Scientist at DataCorp (2016-2018)",
                    "details": [
                        "Built predictive models for customer behavior analysis",
                        "Implemented recommendation systems using collaborative filtering",
                        "Optimized machine learning pipelines for large-scale data processing"
                    ]
                }
            ]
        }
    ]
    
    # Limit to requested count
    candidates = candidates[:min(count, len(candidates))]
    
    created_files = []
    
    # Create a PDF for each candidate
    for i, candidate in enumerate(candidates):
        output_path = os.path.join(output_dir, f"resume_{i+1}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6
        )
        
        normal_style = styles["Normal"]
        
        # Build the content
        content = []
        
        # Personal Information
        content.append(Paragraph(candidate["name"], title_style))
        content.append(Paragraph(f"Email: {candidate['email']} | Phone: {candidate['phone']} | Gender: {candidate['gender']}", normal_style))
        content.append(Spacer(1, 12))
        
        # Education
        content.append(Paragraph("Education", heading_style))
        for edu in candidate["education"]:
            content.append(Paragraph(edu, normal_style))
        content.append(Spacer(1, 12))
        
        # Skills
        content.append(Paragraph("Skills", heading_style))
        content.append(Paragraph(candidate["skills"], normal_style))
        content.append(Spacer(1, 12))
        
        # Experience
        content.append(Paragraph("Experience", heading_style))
        
        for exp in candidate["experience"]:
            content.append(Paragraph(f"<b>{exp['title']}</b>", normal_style))
            for detail in exp["details"]:
                content.append(Paragraph(f"• {detail}", normal_style))
            content.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(content)
        created_files.append(output_path)
    
    print(f"Created {len(created_files)} sample resume PDFs in: {output_dir}")
    return created_files

if __name__ == "__main__":
    # Create a single sample resume
    create_sample_resume()
    
    # Create multiple sample resumes
    create_multiple_sample_resumes(3)