import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_admin_connection():
    """Connect to PostgreSQL with admin credentials"""
    try:
        # You'll need to provide your actual postgres password here
        postgres_password = input("Enter your PostgreSQL 'postgres' user password: ")
        
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password=postgres_password,
            port=5432
        )
        return conn
    except Exception as e:
        print(f"Failed to connect as admin: {e}")
        return None

def fix_database_issues():
    """Fix common database setup issues"""
    
    print("Attempting to fix database issues...")
    
    admin_conn = get_admin_connection()
    if not admin_conn:
        return False
    
    try:
        cursor = admin_conn.cursor()
        admin_conn.autocommit = True
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = 'fingerprint_user'")
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print("Creating fingerprint_user...")
            cursor.execute("CREATE USER fingerprint_user WITH PASSWORD 'securepassword123'")
            print("✅ User created")
        else:
            print("✅ User already exists")
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'fingerprint_db'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print("Creating fingerprint_db...")
            cursor.execute("CREATE DATABASE fingerprint_db")
            print("✅ Database created")
        else:
            print("✅ Database already exists")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE fingerprint_db TO fingerprint_user")
        # Grant schema privileges
        print("Granting schema privileges...")
        cursor.execute("GRANT ALL ON SCHEMA public TO fingerprint_user")
        cursor.execute("ALTER SCHEMA public OWNER TO fingerprint_user")
        
        # Connect to the specific database to grant table privileges
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'fingerprint_db'
            AND pid <> pg_backend_pid()
        """)
        
        cursor.close()
        admin_conn.close()
        
        # Now test the application connection
        test_app_connection()
        
        return True
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        return False

def test_app_connection():
    """Test connection with application credentials"""
    try:
        database_url = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Application connection successful! PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Application connection still failing: {e}")
        return False

if __name__ == "__main__":
    print("Fixing PostgreSQL database setup...")
    success = fix_database_issues()
    
    if success:
        print("\n🎉 Database issues fixed! You can now run your application.")
    else:
        print("\n💥 Could not fix database issues automatically.")
        print("Please check your PostgreSQL installation and try again.")