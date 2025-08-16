import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def select_pdf_file():
    """
    Open a file dialog to select a PDF file
    
    Returns:
        tuple: (file_path, extracted_text) or (None, None) if canceled or error
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select Resume PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not file_path:  # User canceled
        return None, None
    
    # Extract text from the selected PDF
    extracted_text = extract_text_from_pdf(file_path)
    
    if not extracted_text:
        messagebox.showerror("Error", "Could not extract text from the PDF. Please try another file.")
        return None, None
    
    return file_path, extracted_text

def save_extracted_text(text, output_dir=None):
    """
    Save extracted text to a file
    
    Args:
        text (str): Text to save
        output_dir (str, optional): Directory to save the file. Defaults to None.
        
    Returns:
        str: Path to the saved file
    """
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a file dialog to select where to save the file
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.asksaveasfilename(
        title="Save Extracted Text",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialdir=output_dir
    )
    
    if not file_path:  # User canceled
        return None
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def batch_process_pdfs(job_description):
    """
    Process multiple PDF resumes against a job description
    
    Args:
        job_description (str): The job description text
        
    Returns:
        list: List of evaluation results for each resume
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Select directory containing PDF resumes
    dir_path = filedialog.askdirectory(title="Select Directory with PDF Resumes")
    
    if not dir_path:  # User canceled
        return []
    
    results = []
    pdf_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        messagebox.showinfo("No PDFs Found", "No PDF files found in the selected directory.")
        return []
    
    # Import here to avoid circular imports
    from main import evaluate_candidate
    
    for pdf_file in pdf_files:
        file_path = os.path.join(dir_path, pdf_file)
        extracted_text = extract_text_from_pdf(file_path)
        
        if extracted_text:
            # Evaluate the candidate
            evaluation = evaluate_candidate(extracted_text, job_description)
            results.append({
                "filename": pdf_file,
                "evaluation": evaluation
            })
    
    return results