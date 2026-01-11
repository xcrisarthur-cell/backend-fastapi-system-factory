import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import getpass
import os

def connect_to_postgres():
    """Try to connect to postgres with various methods."""
    
    # Method 1: Try current system user (standard Homebrew setup) - No Password
    current_user = os.getenv('USER') or os.getlogin()
    print(f"🔄 Mencoba login sebagai system user '{current_user}' (tanpa password)...")
    try:
        con = psycopg2.connect(
            user=current_user,
            host="localhost",
            port="5432",
            database="postgres"
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("✅ Berhasil login sebagai system user!")
        return con
    except Exception as e:
        print(f"   Gagal: {e}")

    # Method 2: Try 'postgres' user with no password or common defaults
    passwords = ["", "postgres", "admin", "123456", "password", "root"]
    
    for password in passwords:
        try:
            print(f"🔄 Mencoba login sebagai 'postgres' (password: '{password}')...")
            con = psycopg2.connect(
                user="postgres",
                password=password,
                host="localhost",
                port="5432",
                database="postgres"
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print("✅ Berhasil login sebagai 'postgres'!")
            return con
        except psycopg2.OperationalError:
            continue

    # Method 3: Prompt User
    print("\n⚠️  Gagal login otomatis.")
    print("Saya sudah mencoba login sebagai:")
    print(f"1. User sistem '{current_user}' (tanpa password)")
    print("2. User 'postgres' (password kosong/default)")
    print("\nJika Anda baru menginstall Postgres via Homebrew, biasanya login user sistem tanpa password berhasil.")
    print("Mungkin database belum siap atau konfigurasi berbeda.")
    
    while True:
        try:
            user_input = input("Masukkan Username Postgres (default: postgres): ").strip() or "postgres"
            pass_input = getpass.getpass(f"Masukkan Password untuk '{user_input}': ")
            
            con = psycopg2.connect(
                user=user_input,
                password=pass_input,
                host="localhost",
                port="5432",
                database="postgres"
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            return con
        except psycopg2.OperationalError as e:
            print(f"❌ Login gagal: {e}")
            print("Coba lagi atau tekan Ctrl+C untuk batal.")

def setup_database():
    print("🐘 Initializing PostgreSQL Database...")
    
    target_user = "massindo"
    target_pass = "mas5indo"
    target_db = "matrix_massindo"

    try:
        con = connect_to_postgres()
        cursor = con.cursor()
        
        # 1. Check/Create User
        cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{target_user}'")
        if not cursor.fetchone():
            print(f"👤 Creating user '{target_user}'...")
            cursor.execute(f"CREATE USER {target_user} WITH PASSWORD '{target_pass}' CREATEDB")
        else:
            print(f"✅ User '{target_user}' already exists.")
            # Ensure password is correct
            cursor.execute(f"ALTER USER {target_user} WITH PASSWORD '{target_pass}'")

        # 2. Check/Create Database
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{target_db}'")
        if not cursor.fetchone():
            print(f"📦 Creating database '{target_db}'...")
            cursor.execute(f"CREATE DATABASE {target_db} OWNER {target_user}")
        else:
            print(f"✅ Database '{target_db}' already exists.")

        print("\n✨ Database setup complete!")
        cursor.close()
        con.close()
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    if not setup_database():
        sys.exit(1)
