# Quick Reference Card

## 🚀 Initial Setup (5 minutes)

1. **Get MaxMind License**: https://www.maxmind.com/en/geolite2/signup
2. **Add to GitHub Secrets**: 
   - Settings → Secrets → Actions → New secret
   - Name: `MAXMIND_LICENSE_KEY`
3. **Run First Update**: Actions → Update MaxMind → Run workflow

## 🔗 Your Database URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb
```

## ⏰ Update Schedule

- **Automatic**: Daily at 2 AM UTC
- **Manual**: Actions tab → Run workflow button
- **Frequency**: MaxMind updates ~first Tuesday of each month

## 📂 Repository Structure

```
.
├── .github/workflows/
│   └── update-database.yml    # GitHub Actions workflow
├── database/
│   ├── GeoLite2-Country.mmdb  # The database (~6-7 MB)
│   └── last_modified.txt       # Update timestamp
├── scripts/
│   ├── update_maxmind.py       # Main update script
│   ├── test_database.py        # Local testing
│   └── download_from_github.py # Download helper
├── README.md                   # Full documentation
├── SETUP.md                    # Setup guide
└── FILE_STRUCTURE.md           # File explanations
```

## 🐍 Python Usage

```python
import requests

url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb"
r = requests.get(url)

with open("GeoLite2-Country.mmdb", "wb") as f:
    f.write(r.content)
```

## 🔧 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set license key
export MAXMIND_LICENSE_KEY="your_key"

# Run update script
python scripts/update_maxmind.py

# Test database (requires: pip install geoip2)
python scripts/test_database.py
```

## ⚙️ Common Configurations

### Change Update Time
Edit `.github/workflows/update-database.yml`:
```yaml
cron: '0 2 * * *'  # Hour Minute Day Month Weekday
```

Examples:
- `0 */6 * * *` = Every 6 hours
- `0 0 * * 0` = Weekly on Sunday
- `0 0 1 * *` = Monthly on 1st

### Use Different Database
Edit `scripts/update_maxmind.py`:
```python
EDITION_ID = "GeoLite2-Country"  # or "GeoLite2-City" or "GeoLite2-ASN"
```

## 🔍 Monitoring

- **Check Status**: Actions tab
- **View Logs**: Click on workflow run
- **Last Update**: Check `database/last_modified.txt`
- **File Size**: ~6-7 MB for Country database

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow fails with "MAXMIND_LICENSE_KEY not set" | Add secret in Settings → Secrets |
| "401 Unauthorized" | Generate new license key |
| Database not accessible | Ensure repo is Public |
| No updates | MaxMind only updates ~monthly |

## 📊 Costs

- **GitHub Actions**: FREE (2,000 minutes/month)
- **MaxMind License**: FREE (GeoLite2)
- **GitHub Storage**: FREE (well under limits)
- **Bandwidth**: FREE (via raw.githubusercontent.com)

## 🎯 Key Files to Remember

1. **SETUP.md** - Full setup walkthrough
2. **README.md** - Complete documentation
3. **FILE_STRUCTURE.md** - Explains each file
4. **.github/workflows/update-database.yml** - Workflow config
5. **scripts/update_maxmind.py** - Main logic

## 📝 Important Notes

- Repository must be **PUBLIC** for free download URL access
- MaxMind license is free forever (GeoLite2 tier)
- Database updates only when MaxMind releases new version
- Each workflow run takes ~1-2 minutes
- No maintenance required after setup!

## 🔐 Security

✅ Never commit license key to repository  
✅ Use GitHub Secrets for sensitive data  
✅ Database file contains no sensitive info  
✅ Public repository is safe for this use case  

## 💡 Tips

- Star the repo to find it easily
- Enable notifications for failed Actions
- Test locally before relying on automation
- Keep license key saved somewhere safe
- Check Actions logs if something seems wrong

## 🌐 Resources

- MaxMind Account: https://www.maxmind.com/en/account
- GeoLite2 Docs: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
- GitHub Actions: https://docs.github.com/en/actions

---

**Need Help?** Check SETUP.md for detailed instructions or open an issue!
