#!/usr/bin/env python3
"""
Helper script to parse PostgreSQL connection string for DBeaver setup
Usage: python parse_db_connection.py
"""

import os
import re
from urllib.parse import urlparse, parse_qs

def parse_connection_string(connection_string):
    """Parse PostgreSQL connection string into components"""
    # Handle both postgres:// and postgresql://
    if connection_string.startswith("postgres://"):
        connection_string = connection_string.replace("postgres://", "postgresql://", 1)
    
    # Parse URL
    parsed = urlparse(connection_string)
    
    # Extract components
    username = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 5432
    database = parsed.path.lstrip('/')
    
    # Parse query parameters
    query_params = parse_qs(parsed.query)
    sslmode = query_params.get('sslmode', ['require'])[0]
    
    return {
        'host': host,
        'port': port,
        'database': database,
        'username': username,
        'password': password,
        'sslmode': sslmode
    }

def print_dbeaver_settings(conn_info):
    """Print DBeaver connection settings in readable format"""
    print("=" * 60)
    print("DBeaver Connection Settings")
    print("=" * 60)
    print(f"Host:     {conn_info['host']}")
    print(f"Port:     {conn_info['port']}")
    print(f"Database: {conn_info['database']}")
    print(f"Username: {conn_info['username']}")
    print(f"Password: {conn_info['password']}")
    print(f"SSL Mode: {conn_info['sslmode']}")
    print("=" * 60)
    print("\nSteps to connect in DBeaver:")
    print("1. New Database Connection → PostgreSQL")
    print("2. Main Tab:")
    print(f"   - Host: {conn_info['host']}")
    print(f"   - Port: {conn_info['port']}")
    print(f"   - Database: {conn_info['database']}")
    print(f"   - Username: {conn_info['username']}")
    print(f"   - Password: {conn_info['password']}")
    print("3. SSL Tab:")
    print("   - ✅ Enable 'Use SSL'")
    print(f"   - SSL Mode: {conn_info['sslmode']}")
    print("4. Test Connection → Finish")
    print("=" * 60)

if __name__ == "__main__":
    # Try to get from environment variable
    connection_string = os.getenv("DATABASE_URL")
    
    if not connection_string:
        print("DATABASE_URL environment variable not found.")
        print("\nPlease provide connection string:")
        connection_string = input("Connection String: ").strip()
    
    if not connection_string:
        print("Error: No connection string provided")
        exit(1)
    
    try:
        conn_info = parse_connection_string(connection_string)
        print_dbeaver_settings(conn_info)
    except Exception as e:
        print(f"Error parsing connection string: {e}")
        print("\nExample connection string format:")
        print("postgresql://username:password@host:port/database?sslmode=require")
        exit(1)






