import os
import shutil

def cleanup():
    """Remove unwanted files and keep only essential files for the web application"""
    print("\n===== Cleaning up project directory =====\n")
    
    # Files to keep
    essential_files = [
        'app.py',
        'main.py',
        'pdf_handler.py',
        'job_roles.py',
        'requirements.txt',
        'README.md'
    ]
    
    # Directories to keep
    essential_dirs = [
        'templates',
        'uploads',
        'sample_pdfs'
    ]
    
    # Get all files in the current directory
    all_files = [f for f in os.listdir() if os.path.isfile(f)]
    all_dirs = [d for d in os.listdir() if os.path.isdir(d) and d != '__pycache__']
    
    # Remove unwanted files
    for file in all_files:
        if file not in essential_files and not file.endswith('.py'):
            try:
                os.remove(file)
                print(f"Removed file: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")
    
    # Remove test files
    for file in all_files:
        if file.startswith('test_') and file != 'test_web_app.py':
            try:
                os.remove(file)
                print(f"Removed test file: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")
    
    # Remove unwanted directories
    for dir_name in all_dirs:
        if dir_name not in essential_dirs:
            try:
                shutil.rmtree(dir_name)
                print(f"Removed directory: {dir_name}")
            except Exception as e:
                print(f"Error removing {dir_name}: {e}")
    
    # Remove __pycache__ directory
    if os.path.exists('__pycache__'):
        try:
            shutil.rmtree('__pycache__')
            print("Removed __pycache__ directory")
        except Exception as e:
            print(f"Error removing __pycache__: {e}")
    
    print("\nCleanup completed. The project now contains only essential files for the web application.")

if __name__ == "__main__":
    cleanup()