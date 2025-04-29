# coding=utf-8
"""
Clean all databases for AlumBot

This script provides a unified interface to clean:
1. SQLite database (content, embeddings, chat history)
2. Chroma vector database (document embeddings)
3. Downloaded files in web/download_dir
4. Any remaining trained data in the system

Running this script will maintain account settings while removing all content.
"""
import os
import sys
import time
import shutil
import sqlite3
from server.constant.constants import STATIC_DIR, LOCAL_FILE_DOWNLOAD_DIR, SQLITE_DB_DIR, SQLITE_DB_NAME, CHROMA_DB_DIR

def clean_downloaded_files():
    """
    Clean all downloaded files in the web/download_dir folder
    Removes all date-based folders and their contents
    """
    try:
        download_dir_path = os.path.join(STATIC_DIR, LOCAL_FILE_DOWNLOAD_DIR)
        
        if not os.path.exists(download_dir_path):
            print(f"[INFO] Download directory '{download_dir_path}' does not exist.")
            return False
        
        # Count files before deletion for reporting
        file_count = 0
        folder_count = 0
        for root, dirs, files in os.walk(download_dir_path):
            file_count += len(files)
            # Only count date-based subdirectories of download_dir
            if root != download_dir_path:
                folder_count += 1
        
        # Create backup of file list if there are files
        if file_count > 0:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = f"download_files_list_{timestamp}.txt"
            with open(backup_file, "w") as f:
                for root, dirs, files in os.walk(download_dir_path):
                    for file in files:
                        f.write(os.path.join(root, file) + "\n")
            print(f"[INFO] File list backup created: {backup_file}")
        
        # Remove date folders within download_dir (YYYY_MM_DD format directories)
        removed_folders = 0
        for item in os.listdir(download_dir_path):
            item_path = os.path.join(download_dir_path, item)
            # Check if it's a directory and matches date format (YYYY_MM_DD)
            if os.path.isdir(item_path) and (len(item) == 10 and item.count('_') == 2):
                try:
                    shutil.rmtree(item_path)
                    print(f"[INFO] Removed directory: {item_path}")
                    removed_folders += 1
                except Exception as e:
                    print(f"[ERROR] Failed to remove directory {item_path}: {e}")
        
        print(f"[SUCCESS] Removed {file_count} files and {removed_folders} date-based folders from download directory.")
        return True
    
    except Exception as e:
        print(f"[ERROR] Error cleaning download directory: {e}")
        return False

def verify_cleaning():
    """
    Verify that all trained data has been completely removed
    """
    print("\n=== Verifying Complete Data Removal ===")
    all_clean = True
    
    # 1. Check SQLite database tables
    try:
        print("[INFO] Verifying SQLite database tables...")
        conn = sqlite3.connect(f"{SQLITE_DB_DIR}/{SQLITE_DB_NAME}")
        cur = conn.cursor()
        
        tables_to_check = [
            "t_sitemap_url_tab", 
            "t_isolated_url_tab", 
            "t_local_file_tab", 
            "t_local_file_chunk_tab", 
            "t_doc_embedding_map_tab"
        ]
        
        for table in tables_to_check:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            if count > 0:
                print(f"[WARNING] Table '{table}' still has {count} records!")
                all_clean = False
                # Try one more forced cleanup
                try:
                    cur.execute(f"DELETE FROM {table}")
                    conn.commit()
                    print(f"[INFO] Forced cleanup of '{table}' attempted.")
                except Exception as e:
                    print(f"[ERROR] Could not clean table '{table}': {e}")
        
        conn.close()
    except Exception as e:
        print(f"[ERROR] Error verifying SQLite database: {e}")
        all_clean = False

    # 2. Check Chroma database
    if os.path.exists(CHROMA_DB_DIR):
        print("[INFO] Verifying Chroma database...")
        
        # Check for any collection directories
        collection_dirs = 0
        for item in os.listdir(CHROMA_DB_DIR):
            if os.path.isdir(os.path.join(CHROMA_DB_DIR, item)):
                collection_dirs += 1
                print(f"[WARNING] Found Chroma collection: {item}")
                try:
                    shutil.rmtree(os.path.join(CHROMA_DB_DIR, item))
                    print(f"[INFO] Forced removal of collection '{item}'.")
                except Exception as e:
                    print(f"[ERROR] Could not remove collection '{item}': {e}")
        
        if collection_dirs > 0:
            all_clean = False
    
    # 3. Check download directory
    download_dir_path = os.path.join(STATIC_DIR, LOCAL_FILE_DOWNLOAD_DIR)
    if os.path.exists(download_dir_path):
        print("[INFO] Verifying download directory...")
        
        # Check for any remaining date folders
        for item in os.listdir(download_dir_path):
            item_path = os.path.join(download_dir_path, item)
            if os.path.isdir(item_path) and (len(item) == 10 and item.count('_') == 2):
                print(f"[WARNING] Found date folder: {item}")
                try:
                    shutil.rmtree(item_path)
                    print(f"[INFO] Forced removal of folder '{item}'.")
                except Exception as e:
                    print(f"[ERROR] Could not remove folder '{item}': {e}")
                all_clean = False
    
    if all_clean:
        print("[SUCCESS] Verification complete. All data has been successfully cleaned!")
    else:
        print("[WARNING] Some data could not be fully cleaned. You may need to manually check.")
    
    return all_clean

if __name__ == "__main__":
    print("=== AlumBot Full Database Cleaning Tool ===")
    print("This tool will clean ALL databases used by AlumBot, including:")
    print("  1. SQLite database (URLs, files, chat history)")
    print("  2. Chroma vector database (embeddings)")
    print("  3. Downloaded files in web/download_dir")
    print("\nWARNING: All content data will be deleted, but user accounts and settings will be preserved.")
    print("WARNING: Make sure AlumBot is not running before proceeding.")
    
    confirmation = input("\nAre you sure you want to proceed? (yes/no): ")
    
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        sys.exit(0)
    
    # Run SQLite database cleaning
    print("\n=== Cleaning SQLite Database ===")
    try:
        import clean_database
        # Override the confirmation prompt in the module
        clean_database.backup_database()
        clean_database.clean_database()
        clean_database.clean_diskcache()
        print("SQLite database cleaning completed successfully.")
    except Exception as e:
        print(f"Error cleaning SQLite database: {e}")
        print("Continuing to next step...")
    
    # Run Chroma database cleaning
    print("\n=== Cleaning Chroma Vector Database ===")
    try:
        import clean_chroma_db
        # Override the confirmation prompt in the module
        clean_chroma_db.backup_chroma_db()
        clean_chroma_db.clean_chroma_db()
        print("Chroma database cleaning completed successfully.")
    except Exception as e:
        print(f"Error cleaning Chroma database: {e}")
        print("Continuing to next step...")
    
    # Clean downloaded files
    print("\n=== Cleaning Downloaded Files ===")
    clean_downloaded_files()
    
    # Verify that all data has been removed
    verify_cleaning()
    
    print("\n=== All Database Cleaning Complete ===")
    print("Your AlumBot database has been reset to a clean state.")
    print("User accounts and settings are preserved.")
    print("You should restart the AlumBot service for changes to take effect.")
    print("\nIf you need to add content again, use the admin interface to upload files or URLs.")