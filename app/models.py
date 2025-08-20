from .database import get_db_connection
from .encryption import AESEncryption

class User:
    def __init__(self, name, national_id):
        self.name = name
        self.national_id = national_id
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, national_id) VALUES (%s, %s) RETURNING id',
            (self.name, self.national_id)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return user_id

class Fingerprint:
    def __init__(self, user_id, template, image_path):
        self.user_id = user_id
        self.template = template
        self.image_path = image_path
        self.encryption = AESEncryption()
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Encrypt template before storing
        encrypted_template = self.encryption.encrypt(str(self.template))
        
        cursor.execute(
            'INSERT INTO fingerprints (user_id, template, image_path) VALUES (%s, %s, %s) RETURNING id',
            (self.user_id, encrypted_template, self.image_path)
        )
        fingerprint_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return fingerprint_id
    
    @staticmethod
    def get_all_templates():
        conn = get_db_connection()
        cursor = conn.cursor()
        encryption = AESEncryption()
        
        cursor.execute('SELECT id, user_id, template FROM fingerprints')
        fingerprints = cursor.fetchall()
        
        templates = {}
        for fp_id, user_id, encrypted_template in fingerprints:
            try:
                decrypted_template = eval(encryption.decrypt(encrypted_template))
                templates[fp_id] = {
                    'template': decrypted_template,
                    'user_id': user_id
                }
            except:
                continue
        
        cursor.close()
        conn.close()
        return templates

class CrimeRecord:
    def __init__(self, user_id, crime_type, description, date_occurred, status):
        self.user_id = user_id
        self.crime_type = crime_type
        self.description = description
        self.date_occurred = date_occurred
        self.status = status
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO crime_records (user_id, crime_type, description, date_occurred, status)
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (self.user_id, self.crime_type, self.description, self.date_occurred, self.status)
        )
        record_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return record_id
    
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM crime_records WHERE user_id = %s ORDER BY date_occurred DESC',
            (user_id,)
        )
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records