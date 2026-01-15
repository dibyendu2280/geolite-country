#!/usr/bin/env python3
"""
Simple script to download the MaxMind database from your GitHub repository.
Update the GITHUB_USERNAME and REPO_NAME variables below.
"""

import requests
import sys
from pathlib import Path

# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================
GITHUB_USERNAME = "YOUR_USERNAME"  # Your GitHub username
REPO_NAME = "YOUR_REPO"            # Your repository name

# ============================================================================
# Don't modify below this line
# ============================================================================

BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/database"
DB_FILENAME = "GeoLite2-Country.mmdb"
DB_URL = f"{BASE_URL}/{DB_FILENAME}"

def download_database(output_path=None):
    """Download the MaxMind database from GitHub."""
    
    if GITHUB_USERNAME == "YOUR_USERNAME" or REPO_NAME == "YOUR_REPO":
        print("ERROR: Please update GITHUB_USERNAME and REPO_NAME in this script!")
        print(f"Edit {__file__} and set your GitHub username and repository name.")
        sys.exit(1)
    
    if output_path is None:
        output_path = Path.cwd() / DB_FILENAME
    else:
        output_path = Path(output_path)
    
    print(f"Downloading from: {DB_URL}")
    print(f"Saving to: {output_path}")
    print()
    
    try:
        response = requests.get(DB_URL, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded:,} / {total_size:,} bytes)", end='', flush=True)
        
        print(f"\n\n✓ Database successfully downloaded!")
        print(f"File: {output_path}")
        print(f"Size: {output_path.stat().st_size:,} bytes")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("\nERROR: Database not found!")
            print("Please check:")
            print("  1. Your GITHUB_USERNAME and REPO_NAME are correct")
            print("  2. Your repository is public")
            print("  3. The database file exists in the repository")
            print(f"  4. Try opening this URL in your browser: {DB_URL}")
        else:
            print(f"\nERROR: HTTP {e.response.status_code}: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Download failed: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"\nERROR: Could not save file: {e}")
        sys.exit(1)

def main():
    """Main function."""
    print("=" * 60)
    print("MaxMind GeoLite2-Country Database Downloader")
    print("=" * 60)
    print()
    
    # Check if custom output path was provided
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        download_database(output_path)
    else:
        download_database()

if __name__ == "__main__":
    main()
