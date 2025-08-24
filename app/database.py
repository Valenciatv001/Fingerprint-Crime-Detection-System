import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

def get_db_connection():
    return psycopg2.connect(current_app.config['DATABASE_URL'])

def init_db(app):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                gender VARCHAR(10),
                national_id VARCHAR(20) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprints (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                template BYTEA NOT NULL,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crime_records (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                crime_type VARCHAR(100),
                description TEXT,
                date_occurred DATE,
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()