from flask import Blueprint, request, jsonify, render_template
import os
from .utils import save_uploaded_file
from .preprocessing import FingerprintPreprocessor
from .feature_extraction import FeatureExtractor
from .matching import FingerprintMatcher
from .models import Fingerprint, CrimeRecord
from .models import User


# Add this debug code to your routes.py temporarily
print(f"Current working directory: {os.getcwd()}")
print(f"Templates directory exists: {os.path.exists('templates')}")
print(f"Files in templates: {os.listdir('templates') if os.path.exists('templates') else 'NOT FOUND'}")

import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)





main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# @main_bp.route('/capture', methods=['POST'])
# def capture_fingerprint():
#     try:
#         if 'fingerprint' not in request.files:
#             return jsonify({'error': 'No file uploaded'}), 400
        
#         file = request.files['fingerprint']
#         user_id = request.form.get('user_id')
        
#         if not user_id:
#             return jsonify({'error': 'User ID required'}), 400
        
#         # Save uploaded file
#         filepath = save_uploaded_file(file)
#         if not filepath:
#             return jsonify({'error': 'Invalid file type'}), 400
        
#         # Preprocess fingerprint
#         preprocessor = FingerprintPreprocessor()
#         preprocessed = preprocessor.preprocess(filepath)
        
#         # Extract features
#         extractor = FeatureExtractor()
#         template = extractor.extract_features(preprocessed)
        
#         # Save to database
#         fingerprint = Fingerprint(user_id, template, filepath)
#         fingerprint_id = fingerprint.save()
        
#         return jsonify({
#             'message': 'Fingerprint captured successfully',
#             'fingerprint_id': fingerprint_id,
#             'template': template
#         }), 201
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500








@main_bp.route('/capture', methods=['POST'])
def capture_fingerprint():
    try:
        if 'fingerprint' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['fingerprint']
        user_id = request.form.get('user_id')
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        purpose = request.form.get('purpose')



        

        if not user_id:
            return jsonify({'error': 'User ID required'}), 400

        # ✅ Create new user if not exists
        user = User(full_name=full_name, gender=gender)
        user_id = user.save()


        # ✅ Save uploaded file
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({'error': 'Invalid file type'}), 400

        # ✅ Preprocess fingerprint
        preprocessor = FingerprintPreprocessor()
        preprocessed = preprocessor.preprocess(filepath)

        # ✅ Extract features
        extractor = FeatureExtractor()
        template = extractor.extract_features(preprocessed)

        # ✅ Save to DB (fingerprint + optional suspect info)
        fingerprint = Fingerprint(user_id, template, filepath)
        fingerprint_id = fingerprint.save()

        # If you want to also save crime record (using "purpose" as description)
        if purpose:
            record = CrimeRecord(
                user_id=user_id,
                crime_type="General Crime",
                description=purpose,
                date_occurred=None,
                status="ACTIVE"
            )
            record.save()

        return jsonify({
            'message': 'Fingerprint captured successfully',
            'fingerprint_id': fingerprint_id,
            'user_id': user_id,
            'full_name': full_name,
            'gender': gender,
            'purpose': purpose,
            'template': template
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/match', methods=['POST'])
def match_fingerprint():
    try:
        if 'fingerprint' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['fingerprint']
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Process query fingerprint
        preprocessor = FingerprintPreprocessor()
        preprocessed = preprocessor.preprocess(filepath)
        
        extractor = FeatureExtractor()
        query_template = extractor.extract_features(preprocessed)
        
        # Get all templates from database
        database_templates = Fingerprint.get_all_templates()
        
        # Match against database
        matcher = FingerprintMatcher()
        
        # Check what method is available and use it
        if hasattr(matcher, 'find_best_match'):
            result = matcher.find_best_match(query_template, 
                                           {k: v['template'] for k, v in database_templates.items()})
        elif hasattr(matcher, 'find_match'):  # If method has different name
            result = matcher.find_match(query_template, 
                                      {k: v['template'] for k, v in database_templates.items()})
        else:
            return jsonify({'error': 'No matching method found in FingerprintMatcher'}), 500
        
        response = {
            'best_match': result.get('best_match'),
            'best_score': float(result.get('best_score', 0)),
            'matches_found': int(result.get('matches_found', 0)),
            'all_matches': result.get('all_matches', [])
        }
        
        if 'matched_user_id' in result:
            response['matched_user_id'] = result['matched_user_id']
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/records/<int:user_id>', methods=['GET'])
def get_criminal_records(user_id):
    try:
        records = CrimeRecord.get_by_user_id(user_id)
        
        formatted_records = []
        for record in records:
            formatted_records.append({
                'id': record[0],
                'crime_type': record[2],
                'description': record[3],
                'date_occurred': record[4].isoformat() if record[4] else None,
                'status': record[5]
            })
        
        return jsonify({
            'user_id': user_id,
            'records': formatted_records,
            'total_records': len(formatted_records)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500