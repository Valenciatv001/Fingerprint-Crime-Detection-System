#!/usr/bin/env python3
"""
Database connection test script for Fingerprint Crime Detection System
Run this to verify PostgreSQL connection before starting the main application
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test the database connection with detailed error reporting"""
    
    print("=" * 60)
    print("Testing PostgreSQL Database Connection")
    print("=" * 60)
    
    # Get database URL from environment variables
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please check your .env file")
        return False
    
    print(f"Database URL: {database_url}")
    
    try:
        # Try to connect to the database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"✅ PostgreSQL Version: {db_version[0]}")
        
        # Check if our database exists and is accessible
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"✅ Current Database: {current_db[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("✅ Tables found in database:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("⚠️  No tables found in database")
            print("   Run the application once to create tables automatically")
        
        # Test basic query on users table (if it exists)
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✅ Users table accessible: {user_count} records found")
        except psycopg2.Error as e:
            print("⚠️  Users table not accessible yet (this is normal if you haven't run the app)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE CONNECTION SUCCESSFUL!")
        print("Your Flask application should now work correctly.")
        print("=" * 60)
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ CONNECTION FAILED: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if database URL is correct in .env file")
        print("3. Verify the database and user exist")
        print("4. Check if password is correct")
        return False
        
    except psycopg2.ProgrammingError as e:
        print(f"�️  DATABASE SETUP ISSUE: {e}")
        print("\nThis might be normal if tables haven't been created yet.")
        print("Run the Flask application once to create tables automatically.")
        return True
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

def check_environment_variables():
    """Check if all required environment variables are set"""
    
    print("\nChecking environment variables...")
    
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'AES_KEY', 'AES_IV']
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("Fingerprint Crime Detection System - Database Test")
    print("This script tests the PostgreSQL connection before running the main app.\n")
    
    # Check environment variables first
    env_ok = check_environment_variables()
    
    if env_ok:
        print("\n" + "-" * 40)
        # Test database connection
        connection_ok = test_database_connection()
        
        if connection_ok:
            print("\n🎉 You're ready to run the application!")
            print("Execute: python app.py")
        else:
            print("\n💥 Please fix the database issues before running the application.")
    else:
        print("\n💥 Please set all required environment variables in your .env file.")