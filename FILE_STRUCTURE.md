# Repository File Structure

This document explains the purpose of each file in the repository.

## Root Files

### README.md
Main documentation with features, setup instructions, usage examples, and troubleshooting.

### SETUP.md
Step-by-step quick setup guide for first-time users.

### LICENSE
MIT License for the repository scripts. Note: MaxMind data has its own license requiring attribution.

### requirements.txt
Python dependencies needed for local development and testing.

### .gitignore
Specifies which files Git should ignore (Python cache, temporary files, etc.)

## .github/workflows/

### update-database.yml
GitHub Actions workflow that:
- Runs daily at 2 AM UTC (configurable)
- Can be manually triggered
- Checks for database updates
- Downloads and commits new versions automatically

## database/

### .gitkeep
Placeholder file to ensure the directory is tracked by Git (removed after first database download)

### GeoLite2-Country.mmdb
The actual MaxMind GeoLite2-Country database file (~6-7 MB).
**Created by the workflow** on first run.

### last_modified.txt
Stores the Last-Modified timestamp from MaxMind to detect updates.
**Created by the workflow** on first run.

## scripts/

### update_maxmind.py
Main Python script that:
- Checks MaxMind's Last-Modified header
- Downloads database only if newer version exists
- Extracts .mmdb file from tar.gz archive
- Updates last_modified.txt
- Used by GitHub Actions workflow

### test_database.py
Example script to test the database locally:
- Requires `geoip2` Python library
- Looks up IP addresses
- Displays country information
- Interactive mode for testing

### download_from_github.py
Helper script to download the database from your GitHub repository:
- Configure with your GitHub username and repo name
- Downloads database to local machine
- Shows download progress
- Useful for applications that need to fetch the database

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Daily at 2 AM UTC or Manual Trigger                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions Workflow (update-database.yml)              │
│  1. Checkout repository                                     │
│  2. Setup Python 3.11                                       │
│  3. Install requests library                                │
│  4. Run update_maxmind.py                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  update_maxmind.py                                          │
│  1. Read MAXMIND_LICENSE_KEY from environment               │
│  2. Check Last-Modified header from MaxMind                 │
│  3. Compare with stored last_modified.txt                   │
│  4. If newer: Download tar.gz                               │
│  5. Extract .mmdb file                                      │
│  6. Update last_modified.txt                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Git Commit & Push                                          │
│  - Auto-commit new database                                 │
│  - Push to GitHub                                           │
│  - Database immediately available via raw.githubusercontent │
└─────────────────────────────────────────────────────────────┘
```

## File Sizes

| File | Approximate Size |
|------|------------------|
| GeoLite2-Country.mmdb | ~6-7 MB |
| update_maxmind.py | ~6 KB |
| update-database.yml | ~1 KB |
| README.md | ~7 KB |
| SETUP.md | ~5 KB |
| All other files | < 5 KB combined |

## Environment Variables

### Required (GitHub Secrets)

- **MAXMIND_LICENSE_KEY**: Your MaxMind license key
  - Must be added to GitHub Secrets
  - Get from: https://www.maxmind.com/en/accounts/current/license-key
  - Used by: update_maxmind.py

### Optional (Local Development)

- **MAXMIND_LICENSE_KEY**: Same as above, for local testing
  - Set with: `export MAXMIND_LICENSE_KEY="your_key"`
  - Only needed if running update_maxmind.py locally

## URLs After Setup

### Database Download URL
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb
```

### Timestamp Check URL
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/last_modified.txt
```

### GitHub Actions Status
```
https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

## Maintenance

### Regular Maintenance
- **None required!** The workflow handles everything automatically.

### Optional Maintenance
- Monitor Actions tab for failures
- Update Python version in workflow if needed
- Adjust cron schedule if desired
- Keep MaxMind license key valid (free tier is permanent)

## Security Notes

- **Never commit your license key** to the repository
- Store it only in GitHub Secrets
- Repository must be public for free raw.githubusercontent.com access
- The database itself contains no sensitive data

## Troubleshooting Files

If something goes wrong, check:

1. **Actions logs**: Click on failed workflow run in Actions tab
2. **last_modified.txt**: Verify it's being updated
3. **GeoLite2-Country.mmdb**: Check file size is ~6-7 MB
4. **.github/workflows/update-database.yml**: Verify workflow syntax
5. **scripts/update_maxmind.py**: Check for Python errors

## Customization

### Change Database Edition
Edit `update_maxmind.py`:
```python
EDITION_ID = "GeoLite2-Country"  # Change to City or ASN
```

### Change Update Frequency
Edit `update-database.yml`:
```yaml
cron: '0 2 * * *'  # Modify cron expression
```

### Change Branch
Edit `update-database.yml`:
```yaml
uses: actions/checkout@v4
with:
  ref: your-branch-name  # Add this line
```
