
from flask import Flask
import os
from .database import init_db
import numpy as np 
import json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.json_encoder = NumpyEncoder  # Add this line
    
    # Explicitly set the template folder path
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    
    init_db(app)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app