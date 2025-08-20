#!/usr/bin/env python3
"""
Test script to verify template loading
"""

from flask import Flask, render_template
import os

# Create a test Flask app
app = Flask(__name__)

# Set the template folder explicitly
app.template_folder = os.path.join(os.getcwd(), 'templates')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Template error: {str(e)}", 500

@app.route('/test')
def test():
    try:
        return render_template('api_test.html')
    except Exception as e:
        return f"Template error: {str(e)}", 500

if __name__ == '__main__':
    print("Testing template loading...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Templates directory: {app.template_folder}")
    print(f"Files in templates: {os.listdir(app.template_folder) if os.path.exists(app.template_folder) else 'NOT FOUND'}")
    
    app.run(debug=True, port=5001)