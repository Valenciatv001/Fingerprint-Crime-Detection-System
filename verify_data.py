# verify_data.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def verify_data():
    """Verify users and records were added correctly"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        print("USERS:")
        print("-" * 40)
        cursor.execute("SELECT id, name, national_id FROM users ORDER BY id")
        users = cursor.fetchall()
        for user_id, name, national_id in users:
            print(f"ID: {user_id}, Name: {name}, National ID: {national_id}")
        
        print("\nCRIME RECORDS:")
        print("-" * 40)
        cursor.execute("""
            SELECT cr.id, cr.user_id, u.name, cr.crime_type, cr.description, cr.status 
            FROM crime_records cr 
            JOIN users u ON cr.user_id = u.id 
            ORDER BY cr.id
        """)
        records = cursor.fetchall()
        for record_id, user_id, user_name, crime_type, description, status in records:
            print(f"Record {record_id}: {crime_type} - {description} ({status})")
            print(f"   User: {user_name} (ID: {user_id})")
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error verifying data: {e}")

if __name__ == "__main__":
    verify_data()