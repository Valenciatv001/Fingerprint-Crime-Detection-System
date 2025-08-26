import psycopg2
from flask import current_app
import json
from datetime import datetime



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



    @staticmethod
    def get_all_templates():
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT id, user_id, template FROM fingerprints')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        templates = {}
        for fid, user_id, template in rows:
            if not template:
                print(f"[WARNING] Skipping fingerprint {fid} because template is NULL")
                continue
            try:
                # Only decode if template is a string
                if isinstance(template, str):
                    decoded_template = json.loads(template)
                elif isinstance(template, dict):
                    decoded_template = template
                else:
                    raise TypeError(f"Unexpected template type for fingerprint {fid}: {type(template)}")

                templates[fid] = {
                    "user_id": user_id,
                    "template": decoded_template
                }
            except Exception as e:
                print(f"[ERROR] Failed to decode template for fingerprint {fid}: {e}")
        return templates


class CrimeRecord:
    def __init__(self, user_id, crime_type, description, date_occurred, status):
        self.user_id = user_id
        self.crime_type = crime_type
        self.description = description
        self.date_occurred = date_occurred or datetime.utcnow().date()
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
