# AI for Detecting and Reducing Bias in Hiring

## Overview
This project implements an AI system that helps detect and reduce bias in the hiring process. It uses natural language processing techniques to analyze job descriptions for biased language and anonymizes resumes to ensure candidates are evaluated purely based on their skills and experience rather than personal attributes.

## Features

### 1. Job Description Bias Analysis
- Detects biased language in job descriptions across multiple categories:
  - Gender bias (male/female-biased terms)
  - Age bias (terms that may discriminate based on age)
  - Ethnicity bias (terms that may show preference for specific backgrounds)
  - Education bias (terms that favor specific educational institutions)
- Provides suggestions for neutral alternatives
- Visualizes bias distribution across categories

### 2. Resume Anonymization
- Removes personal identifiers from resumes:
  - Names
  - Email addresses
  - Phone numbers
  - Gender indicators
  - Ethnicity indicators
  - University names
- Creates anonymized versions that focus on skills and experience
- **Now supports PDF resume uploads**

### 3. Skill-Based Candidate Evaluation
- Extracts skills from resumes and job descriptions
- Calculates semantic similarity between resume and job description
- Determines skill match percentage
- Identifies matching skills between candidate and job requirements
- Provides fair evaluation metrics based on qualifications, not personal attributes
- **Now supports PDF resume uploads**

### 4. PDF Resume Processing
- Upload and process resumes in PDF format
- Extract text content from PDF documents
- Batch process multiple PDF resumes against a job description
- Rank candidates based on skill match and semantic similarity

### 5. Interactive User Interface
- Menu-driven interface for easy navigation
- Options to analyze job descriptions, anonymize resumes, and evaluate candidates
- Support for loading custom job descriptions and resumes
- File dialog for selecting PDF resumes

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```
python main.py
```

The program will display a menu with the following options:
1. Analyze Job Description for Bias
2. Anonymize Resume (Text or PDF)
3. Evaluate Candidate for Job (Text or PDF)
4. Batch Process PDF Resumes
5. Exit

### PDF Resume Support
To generate sample PDF resumes for testing, run:
```
python create_sample_pdf.py
```
This will create sample PDF resumes in the `sample_pdfs` directory.

## Project Structure

```
├── job_descriptions/     # Sample and user-created job descriptions
│   ├── job1.txt          # Sample job description 1
│   └── job2.txt          # Sample job description 2 (with biased language)
├── main.py               # Main application code
├── pdf_handler.py        # Module for handling PDF resume uploads
├── create_sample_pdf.py  # Script to generate sample PDF resumes
├── sample_pdfs/          # Directory for sample PDF resumes
├── requirements.txt      # Required Python packages
├── sample_resume.txt     # Sample resume for demonstration
└── README.md             # Project documentation
```

## Future Enhancements

- Machine learning model for more accurate skill matching
- Web interface for easier interaction
- Integration with applicant tracking systems
- More sophisticated bias detection algorithms
- Support for additional languages
- Improved PDF parsing with better text extraction
- Support for more document formats (DOCX, HTML, etc.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.