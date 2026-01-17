import os
import re
import sys

# Define target directories
TARGET_DIRS = ["src", "scripts", "examples"]
SKIP_EXTENSIONS = [".pyc", ".png", ".jpg", ".git", ".db"]

def is_binary(file_path):
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read()
            return False
    except:
        return True

def clean_file(filepath):
    # 1. SELF PROTECTION: Do not touch this script itself
    if os.path.abspath(filepath) == os.path.abspath(__file__):
        return

    # Skip binaries
    if is_binary(filepath):
        return

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 2. THE CLEANER: Remove all non-ASCII characters
        # This kills emojis, special symbols, everything > 127
        new_content = re.sub(r'[^\x00-\x7F]+', '', content)
        
        if content != new_content:
            print(f"[CLEANED] {filepath}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception as e:
        print(f"[ERROR] Could not process {filepath}: {e}")

def main():
    print("Starting ASCII Normalization (Emoji Killer)...")
    root_dir = os.getcwd()
    
    for target_dir in TARGET_DIRS:
        full_path = os.path.join(root_dir, target_dir)
        if not os.path.exists(full_path):
            continue
            
        for root, dirs, files in os.walk(full_path):
            # Skip hidden dirs like .venv, __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if any(file.endswith(ext) for ext in SKIP_EXTENSIONS):
                    continue
                    
                file_path = os.path.join(root, file)
                clean_file(file_path)

    print("Normalization Complete.")

if __name__ == "__main__":
    main()