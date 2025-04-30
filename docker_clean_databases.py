#!/usr/bin/env python3
"""
AlumBot Docker Database Cleaning Script
This version is specifically designed for running non-interactively within Docker builds.
It automatically proceeds with cleaning all databases without asking for confirmation.
"""

import os
import shutil
import datetime
import sqlite3
from pathlib import Path

# Directory paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DIR = os.path.join(SCRIPT_DIR, 'sqlite_dir')
CHROMA_DIR = os.path.join(SCRIPT_DIR, 'chroma_dir')
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, 'web', 'download_dir')
DISKCACHE_DIR = os.path.join(SCRIPT_DIR, 'diskcache_dir')

# SQLite database file
SQLITE_DB_FILE = os.path.join(SQLITE_DIR, 'alumBot.db')

print("=== AlumBot Docker Database Cleaning Tool ===")
print("Running in non-interactive mode for Docker build")
print("This tool will clean ALL databases used by AlumBot, including:")
print("  1. SQLite database (URLs, files, chat history)")
print("  2. Chroma vector database (embeddings)")
print("  3. Downloaded files in web/download_dir")
print("  4. Disk cache")
print("")

# Ensure directories exist
os.makedirs(SQLITE_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, 'web'), exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(DISKCACHE_DIR, exist_ok=True)

# Clean the SQLite database
print("\nCleaning SQLite database...")

if os.path.exists(SQLITE_DB_FILE):
    # Backup the database
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_db_file = f"{SQLITE_DB_FILE}.backup_{timestamp}"
    shutil.copy2(SQLITE_DB_FILE, backup_db_file)
    print(f"SQLite database backup created: {backup_db_file}")
    
    # Connect to the database
    conn = sqlite3.connect(SQLITE_DB_FILE)
    cursor = conn.cursor()
    
    # Tables to clear (delete all rows but keep structure)
    tables_to_clear = [
        'tb_crawl_url', 
        'tb_crawl_url_content',
        'tb_isolated_url', 
        'tb_isolated_url_content',
        'tb_local_file', 
        'tb_local_file_content',
        'tb_user_conversation', 
        'tb_user_query_history'
    ]
    
    # Clear each table
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        except sqlite3.Error as e:
            print(f"Error clearing table {table}: {e}")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("SQLite database cleaned successfully")
else:
    print("SQLite database does not exist yet, nothing to clean")

# Clean the Chroma vector database
print("\nCleaning Chroma vector database...")
if os.path.exists(CHROMA_DIR):
    # Backup the Chroma directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_chroma_dir = f"{CHROMA_DIR}_backup_{timestamp}"
    
    try:
        shutil.copytree(CHROMA_DIR, backup_chroma_dir)
        print(f"Chroma database backup created: {backup_chroma_dir}")
        
        # Remove all files from Chroma directory
        for item in os.listdir(CHROMA_DIR):
            item_path = os.path.join(CHROMA_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        print("Chroma database cleaned successfully")
    except Exception as e:
        print(f"Error cleaning Chroma database: {e}")
else:
    print("Chroma directory does not exist yet, nothing to clean")

# Clean the download directory
print("\nCleaning download directory...")
if os.path.exists(DOWNLOAD_DIR):
    try:
        # Remove all files and subdirectories
        for item in os.listdir(DOWNLOAD_DIR):
            item_path = os.path.join(DOWNLOAD_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        print("Download directory cleaned successfully")
    except Exception as e:
        print(f"Error cleaning download directory: {e}")
else:
    print("Download directory does not exist yet, nothing to clean")

# Clean the disk cache directory
print("\nCleaning disk cache...")
if os.path.exists(DISKCACHE_DIR):
    try:
        # Remove all files and subdirectories
        for item in os.listdir(DISKCACHE_DIR):
            item_path = os.path.join(DISKCACHE_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        print("Disk cache cleaned successfully")
    except Exception as e:
        print(f"Error cleaning disk cache: {e}")
else:
    print("Disk cache directory does not exist yet, nothing to clean")

print("\nAll AlumBot databases cleaned successfully")
print("You'll need to repopulate your knowledge base using the admin interface")
print("Note: User accounts, configuration, and interventions have been preserved")