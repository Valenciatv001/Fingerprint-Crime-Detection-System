
#!/usr/bin/env python3
"""
Simplified Fingerprint Crime Detection System
Works without external dependencies in WebContainer
"""

import os
import json
import time
import base64
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Simple in-memory database
DATABASE = {
    'users': [],
    'fingerprints': [],
    'crime_records': [],
    'match_logs': []
}

class SimpleEncryption:
    """Simple encryption using base64 (for demo purposes)"""
    
    def encrypt_template(self, data):
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()
    
    def decrypt_template(self, encrypted_data):
        return base64.b64decode(encrypted_data.encode())

class FingerprintProcessor:
    """Simplified fingerprint processing"""
    
    def __init__(self):
        self.encryption = SimpleEncryption()
    
    def process_fingerprint(self, image_data):
        """Simulate fingerprint processing"""
        # Create a simple hash-based template
        template = {
            'minutiae': [
                {'x': 100, 'y': 100, 'type': 'ending', 'angle': 0.5},
                {'x': 150, 'y': 120, 'type': 'bifurcation', 'angle': 1.2},
                {'x': 200, 'y': 180, 'type': 'ending', 'angle': 2.1}
            ],
            'quality': 0.85,
            'hash': hashlib.md5(image_data.encode() if isinstance(image_data, str) else image_data).hexdigest()
        }
        return json.dumps(template)
    
    def calculate_similarity(self, template1, template2):
        """Calculate similarity between templates"""
        try:
            t1 = json.loads(template1)
            t2 = json.loads(template2)
            
            # Simple similarity based on hash and minutiae count
            if t1.get('hash') == t2.get('hash'):
                return 1.0
            
            minutiae1 = t1.get('minutiae', [])
            minutiae2 = t2.get('minutiae', [])
            
            if not minutiae1 or not minutiae2:
                return 0.0
            
            # Simple distance-based similarity
            total_distance = 0
            matches = 0
            
            for m1 in minutiae1:
                for m2 in minutiae2:
                    distance = ((m1['x'] - m2['x'])**2 + (m1['y'] - m2['y'])**2)**0.5
                    if distance < 20:  # Close enough
                        matches += 1
                        total_distance += distance
                        break
            
            if matches == 0:
                return 0.0
            
            similarity = matches / max(len(minutiae1), len(minutiae2))
            distance_factor = 1.0 - (total_distance / matches / 100.0)
            
            return max(0.0, min(1.0, similarity * distance_factor))
        
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

class FingerprintAPI(BaseHTTPRequestHandler):
    """Simple HTTP API for fingerprint operations"""
    
    def __init__(self, *args, **kwargs):
        self.processor = FingerprintProcessor()
        super().__init__(*args, **kwargs)

    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': time.time(),
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif parsed_path.path.startswith('/records/'):
            user_id = parsed_path.path.split('/')[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Find user records
            user_records = [r for r in DATABASE['crime_records'] if str(r.get('user_id')) == user_id]
            user_info = next((u for u in DATABASE['users'] if str(u.get('id')) == user_id), None)
            
            response = {
                'user': user_info,
                'crime_records': user_records
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            if parsed_path.path == '/capture':
                self.handle_capture(post_data)
            elif parsed_path.path == '/match':
                self.handle_match(post_data)
            elif parsed_path.path == '/add_crime_record':
                self.handle_add_crime_record(post_data)
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def handle_capture(self, post_data):
        """Handle fingerprint capture"""
        try:
            # Simulate fingerprint data (in real implementation, this would be image data)
            fingerprint_data = f"fingerprint_data_{time.time()}"
            
            # Process fingerprint
            template = self.processor.process_fingerprint(fingerprint_data)
            encrypted_template = self.processor.encryption.encrypt_template(template)
            
            # Create user if needed
            user_id = len(DATABASE['users']) + 1
            user = {
                'id': user_id,
                'name': f'User_{user_id}',
                'email': f'user{user_id}@example.com',
                'created_at': time.time()
            }
            DATABASE['users'].append(user)
            
            # Store fingerprint
            fingerprint_id = len(DATABASE['fingerprints']) + 1
            fingerprint = {
                'id': fingerprint_id,
                'user_id': user_id,
                'template_data': encrypted_template,
                'quality_score': 0.85,
                'minutiae_count': 3,
                'created_at': time.time()
            }
            DATABASE['fingerprints'].append(fingerprint)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'fingerprint_id': fingerprint_id,
                'user_id': user_id,
                'quality_score': 0.85,
                'minutiae_count': 3,
                'processing_time': 0.1
            }
            self.wfile.write(json.dumps(response).encode())
        
        except Exception as e:
            self.send_error(500, f"Capture error: {str(e)}")
    
    def handle_match(self, post_data):
        """Handle fingerprint matching"""
        try:
            # Simulate query fingerprint
            query_data = f"query_fingerprint_{time.time()}"
            query_template = self.processor.process_fingerprint(query_data)
            
            best_match = None
            best_score = 0.0
            threshold = 0.8
            
            # Compare with stored fingerprints
            for fp in DATABASE['fingerprints']:
                try:
                    stored_template = self.processor.encryption.decrypt_template(fp['template_data']).decode()
                    score = self.processor.calculate_similarity(query_template, stored_template)
                    
                    if score > best_score and score >= threshold:
                        best_score = score
                        best_match = fp
                except Exception as e:
                    print(f"Error comparing fingerprint {fp['id']}: {e}")
                    continue
            
            # Prepare response
            response = {
                'matched': best_match is not None,
                'similarity_score': best_score,
                'processing_time': 0.2,
                'crime_records': []
            }
            
            if best_match:
                response['user_id'] = best_match['user_id']
                user = next((u for u in DATABASE['users'] if u['id'] == best_match['user_id']), None)
                response['user_name'] = user['name'] if user else 'Unknown'
                
                # Get crime records
                crime_records = [r for r in DATABASE['crime_records'] if r['user_id'] == best_match['user_id']]
                response['crime_records'] = crime_records
            
            # Log match attempt
            log_entry = {
                'id': len(DATABASE['match_logs']) + 1,
                'matched_user_id': response.get('user_id'),
                'similarity_score': best_score,
                'match_result': response['matched'],
                'processing_time': response['processing_time'],
                'created_at': time.time()
            }
            DATABASE['match_logs'].append(log_entry)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        except Exception as e:
            self.send_error(500, f"Match error: {str(e)}")
    
    def handle_add_crime_record(self, post_data):
        """Handle adding crime records"""
        try:
            data = json.loads(post_data)
            
            record_id = len(DATABASE['crime_records']) + 1
            record = {
                'id': record_id,
                'user_id': data.get('user_id'),
                'crime_type': data.get('crime_type'),
                'description': data.get('description'),
                'case_number': data.get('case_number'),
                'location': data.get('location'),
                'status': 'ACTIVE',
                'created_at': time.time()
            }
            DATABASE['crime_records'].append(record)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'record_id': record_id
            }
            self.wfile.write(json.dumps(response).encode())
        
        except Exception as e:
            self.send_error(500, f"Add record error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def create_sample_data():
    """Create some sample data for testing"""
    processor = FingerprintProcessor()
    
    # Create sample users
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'created_at': time.time()},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'created_at': time.time()},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'created_at': time.time()}
    ]
    DATABASE['users'].extend(users)
    
    # Create sample fingerprints
    for i, user in enumerate(users):
        template = processor.process_fingerprint(f"sample_fingerprint_{i}")
        encrypted_template = processor.encryption.encrypt_template(template)
        
        fingerprint = {
            'id': i + 1,
            'user_id': user['id'],
            'template_data': encrypted_template,
            'quality_score': 0.8 + i * 0.05,
            'minutiae_count': 3 + i,
            'created_at': time.time()
        }
        DATABASE['fingerprints'].append(fingerprint)
    
    # Create sample crime records
    crime_records = [
        {
            'id': 1,
            'user_id': 1,
            'crime_type': 'Theft',
            'description': 'Shoplifting incident',
            'case_number': 'CASE001',
            'location': 'Downtown Mall',
            'status': 'ACTIVE',
            'created_at': time.time()
        },
        {
            'id': 2,
            'user_id': 2,
            'crime_type': 'Burglary',
            'description': 'Residential break-in',
            'case_number': 'CASE002',
            'location': 'Oak Street',
            'status': 'ACTIVE',
            'created_at': time.time()
        }
    ]
    DATABASE['crime_records'].extend(crime_records)

def run_server():
    """Run the HTTP server"""
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, FingerprintAPI)
    print(f"Fingerprint Crime Detection System running on http://localhost:5000")
    print("Available endpoints:")
    print("  GET  /health - System health check")
    print("  POST /capture - Capture fingerprint")
    print("  POST /match - Match fingerprint")
    print("  POST /add_crime_record - Add crime record")
    print("  GET  /records/<user_id> - Get user records")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    # Create sample data
    create_sample_data()
    
    # Start server
    run_server()