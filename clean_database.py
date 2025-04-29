# coding=utf-8
import os
import sqlite3
import time
import shutil
from datetime import datetime

# Import constants from the project
from server.constant.constants import SQLITE_DB_DIR, SQLITE_DB_NAME
from server.app.utils.diskcache_client import diskcache_client

# Backup the database before cleaning
def backup_database():
    source = f"{SQLITE_DB_DIR}/{SQLITE_DB_NAME}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = f"{SQLITE_DB_DIR}/{SQLITE_DB_NAME}_backup_{timestamp}"
    
    try:
        shutil.copy2(source, destination)
        print(f"Database backup created: {destination}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to backup database: {e}")
        return False

# Clean the database tables while preserving essential data
def clean_database():
    conn = None
    try:
        conn = sqlite3.connect(f"{SQLITE_DB_DIR}/{SQLITE_DB_NAME}")
        cur = conn.cursor()
        
        # Begin transaction
        conn.execute("BEGIN TRANSACTION")
        
        # 1. Clean sitemap-related tables (reset to empty state)
        print("[INFO] Cleaning sitemap tables...")
        cur.execute("DELETE FROM t_sitemap_url_tab")
        cur.execute("DELETE FROM t_sitemap_domain_tab")
        
        # 2. Clean isolated URL table
        print("[INFO] Cleaning isolated URL table...")
        cur.execute("DELETE FROM t_isolated_url_tab")
        
        # 3. Clean local file tables
        print("[INFO] Cleaning local file tables...")
        cur.execute("DELETE FROM t_local_file_tab")
        cur.execute("DELETE FROM t_local_file_chunk_tab")
        
        # 4. Clean document embedding map
        print("[INFO] Cleaning document embedding tables...")
        cur.execute("DELETE FROM t_doc_embedding_map_tab")
        
        # 5. Clean user QA records (chat history)
        print("[INFO] Cleaning chat history...")
        cur.execute("DELETE FROM t_user_qa_record_tab")
        
        # 6. Verify no trained data remains by checking all related tables
        print("[INFO] Verifying cleanup of trained data...")
        tables_to_verify = [
            "t_sitemap_url_tab", 
            "t_isolated_url_tab", 
            "t_local_file_tab", 
            "t_local_file_chunk_tab", 
            "t_doc_embedding_map_tab"
        ]
        
        for table in tables_to_verify:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            if count > 0:
                print(f"[WARNING] {table} still has {count} records. Attempting deeper cleanup...")
                cur.execute(f"DELETE FROM {table}")
                conn.commit()
        
        # 7. Reset any sequence counters for tables we've cleared
        # This helps ensure new entries start with fresh IDs
        print("[INFO] Resetting table sequence counters...")
        for table in tables_to_verify:
            try:
                cur.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table}'")
            except Exception as table_e:
                print(f"[INFO] Could not reset sequence for {table}: {table_e}")
        
        # NOTE: We're NOT deleting from these tables to preserve configuration:
        # - t_account_tab (admin accounts)
        # - t_bot_setting_tab (bot configuration)
        # - t_user_qa_intervene_tab (manual interventions)
        
        # Commit the transaction
        conn.commit()
        print("[SUCCESS] Database cleaned successfully!")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Error cleaning database: {e}")
    finally:
        if conn:
            conn.close()

# Clean the disk cache
def clean_diskcache():
    try:
        print("[INFO] Cleaning disk cache...")
        keys_to_keep = ["alumBot:bot_setting"]  # Keys we want to preserve
        
        # Instead of iterating directly, use the .get method to check if keys exist
        # and then delete them if they don't need to be preserved
        try:
            # Check if bot_setting exists and preserve it
            bot_setting = diskcache_client.get("alumBot:bot_setting")
            
            # Clear all cache entries
            diskcache_client.clear()
            
            # Restore the setting we want to keep
            if bot_setting is not None:
                diskcache_client.set("alumBot:bot_setting", bot_setting)
                print("[INFO] Preserved bot settings in disk cache")
        except Exception as cache_error:
            print(f"[WARNING] Error during disk cache operations: {cache_error}")
            # Alternative approach if clear() is not working
            print("[INFO] Attempting alternative disk cache cleaning approach...")
            try:
                # Get all keys through the internal database
                import sqlite3
                from os import path
                from server.constant.constants import DISKCACHE_DIR
                
                db_path = path.join(DISKCACHE_DIR, "cache.db")
                if path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Get the bot setting value first if it exists
                    cursor.execute("SELECT value FROM Cache WHERE key = ?", ("alumBot:bot_setting",))
                    setting_row = cursor.fetchone()
                    
                    # Delete all entries except the ones we want to keep
                    preserved = []
                    for key in keys_to_keep:
                        cursor.execute("SELECT key FROM Cache WHERE key = ?", (key,))
                        if cursor.fetchone():
                            preserved.append(key)
                            cursor.execute("SELECT value FROM Cache WHERE key = ?", (key,))
                    
                    # Now delete everything
                    cursor.execute("DELETE FROM Cache WHERE key NOT IN ({})".format(
                        ','.join(['?'] * len(keys_to_keep))), keys_to_keep)
                    
                    conn.commit()
                    conn.close()
                    print(f"[INFO] Preserved {len(preserved)} settings while cleaning disk cache")
                else:
                    print("[WARNING] Cache database file not found")
            except Exception as db_error:
                print(f"[WARNING] Error during alternative disk cache cleaning: {db_error}")
                print("[WARNING] Unable to clean disk cache completely")
                
        print("[SUCCESS] Disk cache cleaned!")
    except Exception as e:
        print(f"[ERROR] Error cleaning disk cache: {e}")
        print("[WARNING] Disk cache may not be completely cleaned")

# Main function
if __name__ == "__main__":
    print("=== AlumBot Database Cleaning Tool ===")
    print("WARNING: This will delete all content data while preserving accounts and settings.")
    confirmation = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        exit()
    
    # Create a backup first
    if backup_database():
        # Clean the database tables
        clean_database()
        # Clean disk cache
        clean_diskcache()
        
        print("\nDatabase cleaning complete.")
        print("You may need to restart the AlumBot service for changes to take effect.")
    else:
        print("Database cleaning aborted due to backup failure.")