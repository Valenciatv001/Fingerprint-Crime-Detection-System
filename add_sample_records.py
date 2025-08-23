# add_sample_records.py
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_sample_users():
    """Add sample users if they don't exist"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Add sample users
            sample_users = [
                ("John Doe", "ID123456"),
                ("Jane Smith", "ID789012"),
                ("Bob Johnson", "ID345678")
            ]
            
            for name, national_id in sample_users:
                cursor.execute(
                    "INSERT INTO users (name, national_id) VALUES (%s, %s) RETURNING id",
                    (name, national_id)
                )
                user_id = cursor.fetchone()[0]
                print(f"Added user {user_id}: {name}")
            
            conn.commit()
            print("✅ Sample users added successfully!")

        elif user_count < 3:
            # Add more sample users
            additional_users = [
                ("Alice Williams", "ID456789"),
                ("Charlie Brown", "ID987654")
            ]

            for name, national_id in additional_users:
                cursor.execute(
                    "INSERT INTO users (name, national_id) VALUES (%s, %s) RETURNING id",
                    (name, national_id)
                )
                user_id = cursor.fetchone()[0]
                print(f"Added user {user_id}: {name}")

            conn.commit()
            print("✅ Additional sample users added successfully!")

        else:
            print(f"ℹ️  Database already has {user_count} users")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error adding sample users: {e}")

def add_sample_records():
    """Add sample criminal records for testing"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # First, make sure we have users
        cursor.execute("SELECT id FROM users ORDER BY id")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        if not user_ids:
            print("❌ No users found in database. Please add users first.")
            return
        
        sample_records = [
            (user_ids[0], "Theft", "Stolen vehicle from parking lot", "2023-01-15", "Solved"),
            (user_ids[0], "Burglary", "Residential break-in", "2023-03-22", "Open"),
            (user_ids[1], "Fraud", "Credit card fraud", "2023-02-10", "Solved"),
            (user_ids[2], "Assault", "Bar fight incident", "2023-04-05", "Open"),
        ]
        
        for user_id, crime_type, description, date_occurred, status in sample_records:
            cursor.execute(
                '''INSERT INTO crime_records (user_id, crime_type, description, date_occurred, status)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                (user_id, crime_type, description, date_occurred, status)
            )
            record_id = cursor.fetchone()[0]
            print(f"Added record {record_id}: {crime_type} for user {user_id}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Sample records added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample records: {e}")

def check_existing_records():
    """Check if records already exist"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM crime_records")
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return count
        
    except Exception as e:
        print(f"❌ Error checking records: {e}")
        return 0

if __name__ == "__main__":
    print("Setting up sample data...")
    
    # First add sample users
    add_sample_users()
    
    # Check if records already exist
    existing_records = check_existing_records()
    
    if existing_records > 0:
        print(f"ℹ️  Database already has {existing_records} crime records")
        response = input("Add more records? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            exit()
    
    # Add sample records
    add_sample_records()
    
    print("\n✅ Sample data setup complete!")













