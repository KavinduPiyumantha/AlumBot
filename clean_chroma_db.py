# coding=utf-8
import os
import shutil
from datetime import datetime

# Get the location of the Chroma database directory
CHROMA_DIR = "chroma_dir"

def backup_chroma_db():
    if not os.path.exists(CHROMA_DIR):
        print(f"[ERROR] Chroma directory '{CHROMA_DIR}' does not exist.")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{CHROMA_DIR}_backup_{timestamp}"
    
    try:
        # Create a full copy of the Chroma directory
        shutil.copytree(CHROMA_DIR, backup_dir)
        print(f"Chroma database backup created: {backup_dir}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to backup Chroma database: {e}")
        return False

def clean_chroma_db():
    try:
        # Check if the directory exists
        if not os.path.exists(CHROMA_DIR):
            print(f"[ERROR] Chroma directory '{CHROMA_DIR}' does not exist.")
            return False
        
        # Instead of trying to modify the database, we'll completely recreate it
        print("[INFO] Completely removing and recreating Chroma database...")
        
        # 1. Remove all collections first
        for item in os.listdir(CHROMA_DIR):
            item_path = os.path.join(CHROMA_DIR, item)
            
            # Skip the SQLite file for now
            if item == "chroma.sqlite3" or item == "chroma.sqlite3-shm" or item == "chroma.sqlite3-wal":
                continue
                
            # Remove collection directories
            if os.path.isdir(item_path):
                print(f"[INFO] Removing collection: {item}")
                shutil.rmtree(item_path)
        
        # 2. Now handle the SQLite database file - delete it completely
        db_path = os.path.join(CHROMA_DIR, "chroma.sqlite3")
        db_shm_path = os.path.join(CHROMA_DIR, "chroma.sqlite3-shm")
        db_wal_path = os.path.join(CHROMA_DIR, "chroma.sqlite3-wal")
        
        # Try to delete the main database file
        retries = 5
        success = False
        
        for attempt in range(retries):
            try:
                # Remove all related SQLite files
                if os.path.exists(db_path):
                    os.remove(db_path)
                if os.path.exists(db_shm_path):
                    os.remove(db_shm_path)
                if os.path.exists(db_wal_path):
                    os.remove(db_wal_path)
                
                success = True
                print("[INFO] Successfully removed Chroma SQLite database files")
                break
            except Exception as e:
                if "being used by another process" in str(e):
                    print(f"[WARNING] Database is locked. Retry attempt {attempt+1}/{retries}")
                    time.sleep(2)  # Wait a bit before retrying
                else:
                    print(f"[WARNING] Failed to remove database file: {e}")
                    break
        
        if not success:
            print("[WARNING] Could not remove Chroma database files. They may be locked by another process.")
            print("[WARNING] Please close any applications using the database and try again.")
            print("[WARNING] Alternatively, restart your computer and run the script again.")
            return False
            
        # Double check to make sure all collections are removed
        any_collections = False
        for item in os.listdir(CHROMA_DIR):
            if os.path.isdir(os.path.join(CHROMA_DIR, item)):
                any_collections = True
                print(f"[WARNING] Collection still exists: {item}")
                
        if any_collections:
            print("[WARNING] Some collections could not be removed. Manual cleanup may be required.")
        else:
            print("[SUCCESS] All embedding collections successfully removed!")
            
        print("[SUCCESS] Chroma vector database cleaned!")
        return True
    except Exception as e:
        print(f"[ERROR] Error cleaning Chroma database: {e}")
        return False

# Main function
if __name__ == "__main__":
    print("=== AlumBot Vector Database Cleaning Tool ===")
    print("WARNING: This will delete all vector embeddings from your Chroma database.")
    confirmation = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        exit()
    
    # Create a backup first
    if backup_chroma_db():
        # Clean the vector database
        if clean_chroma_db():
            print("\nVector database cleaning complete.")
            print("You may need to restart the AlumBot service for changes to take effect.")
        else:
            print("Vector database cleaning failed.")
    else:
        print("Vector database cleaning aborted due to backup failure.")