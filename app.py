

from app import create_app
import os

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

app = create_app()

if __name__ == '__main__':
    # Explicitly set template folder for the main app
    app.template_folder = os.path.join(os.getcwd(), 'templates')
    app.run(debug=True, host='0.0.0.0', port=5000)