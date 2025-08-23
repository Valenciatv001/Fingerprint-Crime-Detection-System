# from .database import get_db_connection
# from .encryption import AESEncryption

# class User:
#     def __init__(self, name, national_id):
#         self.name = name
#         self.national_id = national_id
    
#     def save(self):
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             'INSERT INTO users (name, national_id) VALUES (%s, %s) RETURNING id',
#             (self.name, self.national_id)
#         )
#         user_id = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return user_id

# class Fingerprint:
#     def __init__(self, user_id, template, image_path):
#         self.user_id = user_id
#         self.template = template
#         self.image_path = image_path
#         self.encryption = AESEncryption()
    
#     def save(self):
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         # Encrypt template before storing
#         encrypted_template = self.encryption.encrypt(str(self.template))
        
#         cursor.execute(
#             'INSERT INTO fingerprints (user_id, template, image_path) VALUES (%s, %s, %s) RETURNING id',
#             (self.user_id, encrypted_template, self.image_path)
#         )
#         fingerprint_id = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return fingerprint_id
    
#     @staticmethod
#     def get_all_templates():
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         encryption = AESEncryption()
        
#         cursor.execute('SELECT id, user_id, template FROM fingerprints')
#         fingerprints = cursor.fetchall()
        
#         templates = {}
#         for fp_id, user_id, encrypted_template in fingerprints:
#             try:
#                 decrypted_template = eval(encryption.decrypt(encrypted_template))
#                 templates[fp_id] = {
#                     'template': decrypted_template,
#                     'user_id': user_id
#                 }
#             except:
#                 continue
        
#         cursor.close()
#         conn.close()
#         return templates

# class CrimeRecord:
#     def __init__(self, user_id, crime_type, description, date_occurred, status):
#         self.user_id = user_id
#         self.crime_type = crime_type
#         self.description = description
#         self.date_occurred = date_occurred
#         self.status = status
    
#     def save(self):
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             '''INSERT INTO crime_records (user_id, crime_type, description, date_occurred, status)
#                VALUES (%s, %s, %s, %s, %s) RETURNING id''',
#             (self.user_id, self.crime_type, self.description, self.date_occurred, self.status)
#         )
#         record_id = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return record_id
    
#     @staticmethod
#     def get_by_user_id(user_id):
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             'SELECT * FROM crime_records WHERE user_id = %s ORDER BY date_occurred DESC',
#             (user_id,)
#         )
#         records = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return records




# import psycopg2
# from flask import current_app

# class User:
#     def __init__(self, full_name, gender=None, national_id=None):
#         self.full_name = full_name
#         self.gender = gender
#         self.national_id = national_id

#     def save(self):
#         conn = psycopg2.connect(current_app.config['DATABASE_URL'])
#         cursor = conn.cursor()

#         cursor.execute('''
#             INSERT INTO users (full_name, gender, national_id)
#             VALUES (%s, %s, %s)
#             RETURNING id
#         ''', (self.full_name, self.gender, self.national_id))

#         user_id = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return user_id

#     @staticmethod
#     def get_by_id(user_id):
#         conn = psycopg2.connect(current_app.config['DATABASE_URL'])
#         cursor = conn.cursor()
#         cursor.execute('SELECT id, full_name, gender, national_id, created_at FROM users WHERE id = %s', (user_id,))
#         row = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         return row


# import psycopg2
# from flask import current_app

# class User:
#     def __init__(self, full_name, gender=None, national_id=None):
#         self.full_name = full_name
#         self.gender = gender
#         self.national_id = national_id

#     def save(self):
#         conn = psycopg2.connect(current_app.config['DATABASE_URL'])
#         cursor = conn.cursor()

#         cursor.execute('''
#             INSERT INTO users (full_name, gender, national_id)
#             VALUES (%s, %s, %s)
#             RETURNING id
#         ''', (self.full_name, self.gender, self.national_id))

#         user_id = cursor.fetchone()[0]
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return user_id

#     @staticmethod
#     def get_by_id(user_id):
#         conn = psycopg2.connect(current_app.config['DATABASE_URL'])
#         cursor = conn.cursor()
#         cursor.execute('SELECT id, full_name, gender, national_id, created_at FROM users WHERE id = %s', (user_id,))
#         row = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         return row


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


class Fingerprint:
    def __init__(self, user_id, template, image_path):
        self.user_id = user_id
        self.template = json.dumps(template)   # store as JSON string
        self.image_path = image_path

    def save(self):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fingerprints (user_id, template, image_path)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', (self.user_id, self.template, self.image_path))
        fid = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return fid

    # @staticmethod
    # def get_all_templates():
    #     conn = get_conn()
    #     cursor = conn.cursor()
    #     cursor.execute('SELECT id, user_id, template FROM fingerprints')
    #     rows = cursor.fetchall()
    #     cursor.close()
    #     conn.close()

    #     templates = {}
    #     for row in rows:
    #         fid, user_id, template = row
    #         templates[fid] = {
    #             "user_id": user_id,
    #             "template": json.loads(template)
    #         }
    #     return templates


    @staticmethod
    def get_all_templates():
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, template FROM fingerprints")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        templates = {}
        aes = AESEncryption()
        for row in rows:
            template_id, user_id, template_data = row

            # Convert memoryview -> bytes -> str -> dict
            if isinstance(template_data, memoryview):
                template_data = template_data.tobytes().decode("utf-8")
            
            # Decrypt if needed
            # decrypted = AESEncryption().decrypt(template_data)

            # template_dict = json.loads(template_data)
            try:
                decrypted = aes.decrypt(template_data)  # 🔑 decrypt
                template_dict = json.loads(decrypted)  # 🔑 now valid JSON
            except Exception as e:
                print(f"[ERROR] Failed to parse template {template_id}: {e}")
            continue

            templates[template_id] = {
                "user_id": user_id,
                "template": template_dict
            }

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
