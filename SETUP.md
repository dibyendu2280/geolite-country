# Quick Setup Guide

Follow these steps to get your MaxMind auto-update repository running in under 5 minutes.

## Step 1: Fork/Clone This Repository

### Option A: Use this as a template
1. Click the "Use this template" button (if available)
2. Name your repository (e.g., `maxmind-geolite2-country`)
3. Choose Public (required for free raw.githubusercontent.com access)
4. Click "Create repository"

### Option B: Clone and push to your own repo
```bash
git clone <this-repo-url>
cd <repo-directory>
git remote remove origin
git remote add origin <your-new-repo-url>
git push -u origin main
```

## Step 2: Get Your MaxMind License Key

1. Go to https://www.maxmind.com/en/geolite2/signup
2. Fill out the registration form (it's free!)
3. Verify your email address
4. Log in to your MaxMind account
5. Navigate to: **Account** → **Manage License Keys**
6. Click **"Generate new license key"**
7. Give it a description: `GitHub Auto-Update`
8. For "Will this key be used for GeoIP Update?": Select **No**
9. Click **Confirm**
10. **IMPORTANT**: Copy your license key immediately (you can't see it again!)

## Step 3: Add License Key to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click the green **"New repository secret"** button
5. Fill in:
   - **Name**: `MAXMIND_LICENSE_KEY` (must be exact!)
   - **Secret**: Paste your MaxMind license key
6. Click **"Add secret"**

## Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If Actions are disabled, click **"I understand my workflows, go ahead and enable them"**
3. You should see the "Update MaxMind GeoLite2 Database" workflow

## Step 5: Run First Update

### Option A: Manual Trigger (Recommended)
1. In the **Actions** tab
2. Click on **"Update MaxMind GeoLite2 Database"** in the left sidebar
3. Click **"Run workflow"** button (top right)
4. Keep `main` branch selected
5. Click the green **"Run workflow"** button
6. Wait 1-2 minutes for completion
7. Refresh the page to see the result

### Option B: Wait for Scheduled Run
- The workflow will automatically run at 2 AM UTC tomorrow
- Check back then to verify it worked

## Step 6: Verify It Worked

After the workflow completes successfully:

1. **Check the database folder**:
   - Navigate to `database/` in your repository
   - You should see:
     - `GeoLite2-Country.mmdb` (~6-7 MB)
     - `last_modified.txt`

2. **Check the commit history**:
   - Look for a commit message like: "Update GeoLite2-Country database - 2025-01-15"
   - It should be made by `github-actions[bot]`

3. **Test the download URL**:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb
   ```
   - Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual values
   - Open this URL in your browser
   - It should start downloading the `.mmdb` file

## Step 7: Use Your Database! 🎉

Your database URL is now:
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb
```

Use it in your applications:

### Python Example
```python
import requests

url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/database/GeoLite2-Country.mmdb"
response = requests.get(url)

with open("GeoLite2-Country.mmdb", "wb") as f:
    f.write(response.content)

print("Database downloaded!")
```

### Test Locally
```bash
cd scripts
python test_database.py
```

## Troubleshooting

### Workflow Failed: "MAXMIND_LICENSE_KEY environment variable not set"
- **Solution**: Make sure you added the secret with the EXACT name `MAXMIND_LICENSE_KEY`
- Secrets are case-sensitive!

### Workflow Failed: HTTP 401 Unauthorized
- **Solution**: Your license key is invalid or expired
- Generate a new license key from MaxMind and update the GitHub secret

### Workflow Succeeded But No Database File
- **Solution**: Check the Actions logs for details
- The workflow might have determined no update was needed
- Try clicking "Run workflow" again

### "This repository doesn't exist" when accessing raw URL
- **Solution**: Make sure your repository is **Public**
- Private repositories require authentication for raw.githubusercontent.com

### Need Help?
- Check the [main README](README.md) for detailed documentation
- Review the Actions logs for error messages
- Open an issue in the repository

## What Happens Next?

✅ Your database will automatically update every day at 2 AM UTC  
✅ Updates only happen when MaxMind releases a new version  
✅ You can always manually trigger an update from the Actions tab  
✅ The download URL will always have the latest version  

## Optional: Test the Update Script Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your license key
export MAXMIND_LICENSE_KEY="your_license_key_here"

# Run the update script
python scripts/update_maxmind.py
```

---

**That's it!** Your MaxMind GeoLite2-Country database is now automatically maintained and publicly accessible. 🌍
