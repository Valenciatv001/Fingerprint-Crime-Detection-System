# check_users.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_users():
    """Check existing users in the database"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, national_id FROM users ORDER BY id")
        users = cursor.fetchall()
        
        print("Existing users in database:")
        print("-" * 40)
        for user_id, name, national_id in users:
            print(f"ID: {user_id}, Name: {name}, National ID: {national_id}")
        
        cursor.close()
        conn.close()
        
        return [user[0] for user in users]  # Return list of user IDs
        
    except Exception as e:
        print(f"Error checking users: {e}")
        return []

if __name__ == "__main__":
    check_users()