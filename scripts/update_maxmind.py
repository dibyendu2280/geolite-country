#!/usr/bin/env python3
"""
MaxMind GeoLite2-Country Database Updater
Checks for updates using Last-Modified header and downloads if newer version available.
"""

import os
import sys
import requests
import tarfile
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
MAXMIND_URL = "https://download.maxmind.com/app/geoip_download"
EDITION_ID = "GeoLite2-Country"
DATABASE_DIR = Path("database")
MMDB_FILE = DATABASE_DIR / "GeoLite2-Country.mmdb"
LAST_MODIFIED_FILE = DATABASE_DIR / "last_modified.txt"

def get_license_key():
    """Get MaxMind license key from environment variable."""
    license_key = os.environ.get('MAXMIND_LICENSE_KEY')
    if not license_key:
        print("ERROR: MAXMIND_LICENSE_KEY environment variable not set!")
        sys.exit(1)
    return license_key

def get_stored_last_modified():
    """Read the stored Last-Modified timestamp."""
    if LAST_MODIFIED_FILE.exists():
        return LAST_MODIFIED_FILE.read_text().strip()
    return None

def save_last_modified(last_modified):
    """Save the Last-Modified timestamp."""
    DATABASE_DIR.mkdir(exist_ok=True)
    LAST_MODIFIED_FILE.write_text(last_modified)

def check_for_updates(license_key):
    """Check if a newer database version is available."""
    params = {
        'edition_id': EDITION_ID,
        'license_key': license_key,
        'suffix': 'tar.gz'
    }
    
    print("Checking for database updates...")
    
    try:
        # Make HEAD request to check Last-Modified header
        response = requests.head(MAXMIND_URL, params=params, timeout=30)
        response.raise_for_status()
        
        current_last_modified = response.headers.get('Last-Modified')
        
        if not current_last_modified:
            print("WARNING: No Last-Modified header found!")
            return False, None
        
        print(f"Remote Last-Modified: {current_last_modified}")
        
        stored_last_modified = get_stored_last_modified()
        
        if stored_last_modified:
            print(f"Stored Last-Modified: {stored_last_modified}")
            
            if current_last_modified == stored_last_modified:
                print("✓ Database is up to date. No download needed.")
                return False, current_last_modified
        else:
            print("No stored Last-Modified found. Will download database.")
        
        print("✓ Update available!")
        return True, current_last_modified
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to check for updates: {e}")
        sys.exit(1)

def download_and_extract(license_key):
    """Download and extract the MaxMind database."""
    params = {
        'edition_id': EDITION_ID,
        'license_key': license_key,
        'suffix': 'tar.gz'
    }
    
    print("\nDownloading database...")
    
    try:
        response = requests.get(MAXMIND_URL, params=params, stream=True, timeout=120)
        response.raise_for_status()
        
        # Save to temporary file
        temp_tar = DATABASE_DIR / "temp.tar.gz"
        DATABASE_DIR.mkdir(exist_ok=True)
        
        # Download with progress
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(temp_tar, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='', flush=True)
        
        print("\n✓ Download complete!")
        
        # Extract .mmdb file
        print("Extracting database...")
        
        with tarfile.open(temp_tar, 'r:gz') as tar:
            # Find the .mmdb file in the archive
            mmdb_member = None
            for member in tar.getmembers():
                if member.name.endswith('.mmdb'):
                    mmdb_member = member
                    break
            
            if not mmdb_member:
                print("ERROR: Could not find .mmdb file in archive!")
                sys.exit(1)
            
            # Extract to temporary location
            tar.extract(mmdb_member, path=DATABASE_DIR / "temp_extract")
            
            # Move to final location
            extracted_path = DATABASE_DIR / "temp_extract" / mmdb_member.name
            shutil.move(str(extracted_path), str(MMDB_FILE))
            
            # Cleanup
            shutil.rmtree(DATABASE_DIR / "temp_extract")
            temp_tar.unlink()
        
        print(f"✓ Database extracted to: {MMDB_FILE}")
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Download failed: {e}")
        sys.exit(1)
    except (tarfile.TarError, OSError) as e:
        print(f"ERROR: Extraction failed: {e}")
        sys.exit(1)

def main():
    """Main execution function."""
    print("=" * 60)
    print("MaxMind GeoLite2-Country Database Updater")
    print("=" * 60)
    print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
    
    license_key = get_license_key()
    
    # Check for updates
    needs_update, last_modified = check_for_updates(license_key)
    
    if needs_update:
        # Download and extract
        download_and_extract(license_key)
        
        # Save the new Last-Modified timestamp
        save_last_modified(last_modified)
        
        print("\n" + "=" * 60)
        print("✓ Database successfully updated!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("No update needed. Exiting.")
        print("=" * 60)

if __name__ == "__main__":
    main()
