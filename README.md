# MaxMind GeoLite2-Country Database Repository

Automatically downloads and maintains the latest MaxMind GeoLite2-Country database using GitHub Actions.

## 🌍 Direct Database Download URL

Once set up, access the database directly at:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual GitHub username and repository name.

## ✨ Features

- ✅ **Automatic daily updates** - Checks every day at 2 AM UTC
- ✅ **Smart update detection** - Uses Last-Modified header to avoid unnecessary downloads
- ✅ **Zero maintenance** - Runs entirely on GitHub Actions
- ✅ **Public access** - Direct download URL for unlimited usage
- ✅ **Version tracking** - Git history shows all updates

## 🚀 Setup Instructions

### 1. Get MaxMind License Key

1. Create a free account at [MaxMind](https://www.maxmind.com/en/geolite2/signup)
2. Log in and navigate to **Account** → **Manage License Keys**
3. Click **Generate new license key**
4. Give it a name (e.g., "GitHub Auto-Update")
5. Select **No** for "Will this key be used for GeoIP Update?"
6. Copy the license key (you'll only see it once!)

### 2. Add License Key to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `MAXMIND_LICENSE_KEY`
5. Value: Paste your MaxMind license key
6. Click **Add secret**

### 3. Initial Setup

The repository needs an initial database download. You have two options:

#### Option A: Manual trigger (Recommended)
1. Go to **Actions** tab in your repository
2. Click on "Update MaxMind GeoLite2 Database" workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for it to complete (~1-2 minutes)

#### Option B: Wait for scheduled run
The workflow will run automatically at 2 AM UTC the next day.

### 4. Verify Setup

After the first run:
1. Check the `database/` directory for `GeoLite2-Country.mmdb`
2. Check the `database/last_modified.txt` file is present
3. Test the direct download URL (see above)

## 📋 How It Works

1. **Daily Check**: GitHub Actions runs every day at 2 AM UTC
2. **Compare Headers**: Script checks MaxMind's Last-Modified header
3. **Download if Newer**: Only downloads if the remote database is newer
4. **Auto-Commit**: New database is automatically committed and pushed
5. **Public Access**: Updated file is immediately available via raw.githubusercontent.com

## 🗂️ Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── update-database.yml    # GitHub Actions workflow
├── database/
│   ├── GeoLite2-Country.mmdb      # The actual database file
│   └── last_modified.txt          # Timestamp of last update
├── scripts/
│   └── update_maxmind.py          # Update script
└── README.md                       # This file
```

## 🔧 Manual Update

To manually trigger an update:

1. Go to **Actions** tab
2. Select "Update MaxMind GeoLite2 Database"
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow**

Or run locally:
```bash
export MAXMIND_LICENSE_KEY="your_license_key_here"
python scripts/update_maxmind.py
```

## 📊 Usage Examples

### Python
```python
import requests
import geoip2.database

# Download the database
url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb"
response = requests.get(url)

with open("GeoLite2-Country.mmdb", "wb") as f:
    f.write(response.content)

# Use it
reader = geoip2.database.Reader("GeoLite2-Country.mmdb")
response = reader.country("8.8.8.8")
print(response.country.iso_code)  # US
reader.close()
```

### Node.js
```javascript
const maxmind = require('maxmind');
const https = require('https');
const fs = require('fs');

const url = 'https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb';

// Download
const file = fs.createWriteStream('GeoLite2-Country.mmdb');
https.get(url, (response) => {
    response.pipe(file);
    file.on('finish', () => {
        file.close();
        
        // Use it
        maxmind.open('GeoLite2-Country.mmdb').then(lookup => {
            console.log(lookup.get('8.8.8.8'));
        });
    });
});
```

### PHP
```php
<?php
require_once 'vendor/autoload.php';

use GeoIp2\Database\Reader;

// Download
$url = 'https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb';
file_put_contents('GeoLite2-Country.mmdb', file_get_contents($url));

// Use it
$reader = new Reader('GeoLite2-Country.mmdb');
$record = $reader->country('8.8.8.8');
echo $record->country->isoCode; // US
?>
```

## ⚙️ Configuration

### Change Update Schedule

Edit `.github/workflows/update-database.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Change this cron expression
```

Common schedules:
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 0 * * 0` - Weekly on Sunday
- `0 0 1 * *` - Monthly on the 1st

### Use Different Database

Edit `scripts/update_maxmind.py`:

```python
EDITION_ID = "GeoLite2-Country"  # Change to:
# "GeoLite2-City" for city-level data
# "GeoLite2-ASN" for ASN data
```

## 📝 Notes

- MaxMind updates GeoLite2 databases typically on the first Tuesday of each month
- The database file is ~6-7 MB (Country edition)
- GitHub has a 100 MB file size limit (Country database is well under this)
- This uses GitHub Actions free tier (2,000 minutes/month for free accounts)
- Each update run uses ~1-2 minutes

## 📜 License

This repository uses MaxMind's GeoLite2 database, which requires attribution:

> This product includes GeoLite2 data created by MaxMind, available from
> [https://www.maxmind.com](https://www.maxmind.com).

The scripts and workflow in this repository are provided as-is for educational purposes.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the update script or documentation.

## 🔗 Resources

- [MaxMind GeoLite2 Free Databases](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GeoIP2 Python Library](https://github.com/maxmind/GeoIP2-python)

## ⚠️ Troubleshooting

### "No Last-Modified header found"
Check that your MaxMind license key is valid and properly set in GitHub Secrets.

### Workflow not running
1. Check Actions are enabled: Settings → Actions → General
2. Verify the workflow file is in `.github/workflows/`
3. Check GitHub Actions logs for errors

### Database not updating
1. Check the Actions logs for errors
2. Verify your license key hasn't expired
3. Ensure GitHub Actions has write permissions

---

Made with ❤️ using GitHub Actions
# geolite-country
