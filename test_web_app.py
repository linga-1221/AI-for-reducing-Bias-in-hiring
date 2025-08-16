import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the web browser after a short delay"""
    webbrowser.open('http://127.0.0.1:5000')

def test_web_app():
    """Test the web application"""
    print("\n===== Testing Web Application =====\n")
    print("Starting Flask web server...")
    print("A browser window should open automatically.")
    print("\nInstructions:")
    print("1. Select a job role from the dropdown")
    print("2. Upload a resume PDF file")
    print("3. Click 'Analyze Resume' to see the results")
    print("\nPress Ctrl+C to stop the server when done.")
    
    # Open browser after a short delay
    Timer(2, open_browser).start()
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    test_web_app()