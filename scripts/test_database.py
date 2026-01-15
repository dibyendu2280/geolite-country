#!/usr/bin/env python3
"""
Example script to test the MaxMind GeoLite2-Country database.
Requires: pip install geoip2
"""

import sys
from pathlib import Path

try:
    import geoip2.database
except ImportError:
    print("ERROR: geoip2 library not installed!")
    print("Install it with: pip install geoip2")
    sys.exit(1)

# Path to database
DB_PATH = Path(__file__).parent.parent / "database" / "GeoLite2-Country.mmdb"

def lookup_ip(ip_address):
    """Look up country information for an IP address."""
    try:
        with geoip2.database.Reader(str(DB_PATH)) as reader:
            response = reader.country(ip_address)
            
            print(f"\n{'='*50}")
            print(f"IP Address: {ip_address}")
            print(f"{'='*50}")
            print(f"Country: {response.country.name}")
            print(f"Country Code: {response.country.iso_code}")
            print(f"Continent: {response.continent.name}")
            print(f"Continent Code: {response.continent.code}")
            print(f"{'='*50}\n")
            
    except geoip2.errors.AddressNotFoundError:
        print(f"ERROR: IP address {ip_address} not found in database")
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    """Main function."""
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Please run the update script first or trigger the GitHub Action.")
        sys.exit(1)
    
    print("\nMaxMind GeoLite2-Country Database Test")
    print("=" * 50)
    
    # Test with some well-known IPs
    test_ips = [
        "8.8.8.8",      # Google DNS - USA
        "1.1.1.1",      # Cloudflare DNS - Australia
        "208.67.222.222", # OpenDNS - USA
    ]
    
    for ip in test_ips:
        lookup_ip(ip)
    
    # Interactive mode
    print("\nEnter an IP address to look up (or 'quit' to exit):")
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if user_input:
                lookup_ip(user_input)
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()
