
import psycopg2
from flask import current_app
import json
from app.encryption import AESEncryption

def get_conn():
    return psycopg2.connect(current_app.config['DATABASE_URL'])


class User:
    def __init__(self, full_name, gender=None, national_id=None):
        self.full_name = full_name
        self.gender = gender
        self.national_id = national_id

    def save(self):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (full_name, gender, national_id)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (self.full_name, self.gender, self.national_id))

        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT id, full_name, gender, national_id, created_at FROM users WHERE id = %s', (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


# class Fingerprint:
#     def __init__(self, user_id, template, image_path):
#         self.user_id = user_id
#         self.template = json.dumps(template)   # store as JSON string
#         self.image_path = image_path

#     def save(self):
#         conn = get_conn()
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO fingerprints (user_id, template, image_path)
#             VALUES (%s, %s, %s)
#             RETURNING id
#         ''', (self.user_id, self.template, self.image_path))
#         fid = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return fid

#     @staticmethod
#     def get_all_templates():
#         conn = get_conn()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, user_id, template FROM fingerprints")
#         rows = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         templates = {}
#         aes = AESEncryption()
#         for row in rows:
#             template_id, user_id, template_data = row

#             # Convert memoryview -> bytes -> str -> dict
#             if isinstance(template_data, memoryview):
#                 template_data = template_data.tobytes().decode("utf-8")
            
          
#             try:
#                 decrypted = aes.decrypt(template_data)  # 🔑 decrypt
#                 template_dict = json.loads(decrypted)  # 🔑 now valid JSON
#             except Exception as e:
#                 print(f"[ERROR] Failed to parse template {template_id}: {e}")
#             continue

#             templates[template_id] = {
#                 "user_id": user_id,
#                 "template": template_dict
#             }

#         return templates


import json
from .database import get_db_connection
from .encryption import AESEncryption


class Fingerprint:
    def __init__(self, user_id, template, image_path):
        self.user_id = user_id
        self.template = template
        self.image_path = image_path

    def save(self):
        """Save fingerprint template and image path to DB"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Convert dict → JSON string
        template_json = json.dumps(self.template)

        # Encrypt JSON string
        aes = AESEncryption()
        encrypted_template = aes.encrypt(template_json)

        cursor.execute("""
            INSERT INTO fingerprints (user_id, template, image_path)
            VALUES (%s, %s, %s) RETURNING id
        """, (self.user_id, encrypted_template, self.image_path))

        fid = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return fid

    @staticmethod
    def get_all_templates():
        """Retrieve all fingerprint templates as Python dicts"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, template FROM fingerprints")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        templates = {}
        aes = AESEncryption()

        for row in rows:
            template_id, user_id, template_data = row

            # Fix psycopg2 memoryview type
            if isinstance(template_data, memoryview):
                template_data = template_data.tobytes().decode("utf-8")
            elif isinstance(template_data, bytes):
                template_data = template_data.decode("utf-8")

            try:
                # Decrypt → Parse JSON
                decrypted = aes.decrypt(template_data)
                template_dict = json.loads(decrypted)

                templates[template_id] = {
                    "user_id": user_id,
                    "template": template_dict
                }

            except Exception as e:
                print(f"[ERROR] Failed to load template {template_id}: {e}")
                continue

        return templates


class CrimeRecord:
    def __init__(self, user_id, crime_type, description, date_occurred, status):
        self.user_id = user_id
        self.crime_type = crime_type
        self.description = description
        self.date_occurred = date_occurred
        self.status = status

    def save(self):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO crime_records (user_id, crime_type, description, date_occurred, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (self.user_id, self.crime_type, self.description, self.date_occurred, self.status))
        record_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return record_id

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM crime_records WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
