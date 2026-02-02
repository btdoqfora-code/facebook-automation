# Facebook Page Automation Setup Guide

## 🎯 What This Does
Automatically posts a variety of engaging content to your Facebook page:
- **📰 Translated Spanish News (50%)** - Uses Gemini AI to translate and summarize
- **🏔️ Quito Content (30%)** - Interesting stories, tips, and photos about Quito
- **😂 Expat Memes (20%)** - Funny, relatable content about expat life

Runs on GitHub Actions (completely free) and posts every 6 hours with randomized content types.

## 📋 Prerequisites
1. Facebook Page (you have this ✓)
2. Facebook App with Page permissions (you have this ✓)
3. Google Gemini API key (free tier available)
4. GitHub account (free)

---

## 🔧 Step-by-Step Setup

### Step 1: Get Your Gemini API Key (5 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key and save it somewhere safe

### Step 2: Get Your Facebook Credentials

You need two things from your Facebook App:

**A) Page ID:**
1. Go to your Facebook page: https://www.facebook.com/profile.php?id=61587517104788
2. Your Page ID is: `61587517104788` (the number in the URL)

**B) Page Access Token:**
1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from the dropdown
3. Click "Get Token" → "Get Page Access Token"
4. Select your page
5. Make sure these permissions are checked:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
6. Copy the access token (starts with "EAA...")

**IMPORTANT:** For long-term automation, you need a long-lived token:
1. Go to: https://developers.facebook.com/tools/debug/accesstoken/
2. Paste your token and click "Debug"
3. Click "Extend Access Token"
4. Copy the new extended token (good for 60 days)

### Step 3: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Name it: `facebook-automation` (or anything you like)
4. Select "Public" (required for free GitHub Actions)
5. Click "Create repository"

### Step 4: Upload Files to GitHub

**Option A - Using GitHub Website (Easier):**
1. In your new repository, click "Add file" → "Upload files"
2. Drag and drop these files:
   - `facebook_automation.py`
   - `requirements.txt`
3. Click "Commit changes"
4. Click "Add file" → "Create new file"
5. Name it: `.github/workflows/facebook_automation.yml`
6. Copy/paste the content from `facebook_automation.yml`
7. Click "Commit changes"

**Option B - Using Git (If you know Git):**
```bash
git clone https://github.com/YOUR-USERNAME/facebook-automation.git
cd facebook-automation
# Copy the files into this directory
git add .
git commit -m "Initial setup"
git push
```

### Step 5: Add Your Secret Keys to GitHub

1. In your GitHub repository, click "Settings" tab
2. In the left sidebar, click "Secrets and variables" → "Actions"
3. Click "New repository secret" and add these three secrets:

**Secret 1:**
- Name: `FACEBOOK_PAGE_ID`
- Value: `61587517104788`

**Secret 2:**
- Name: `FACEBOOK_ACCESS_TOKEN`
- Value: Your page access token from Step 2 (starts with EAA...)

**Secret 3:**
- Name: `GEMINI_API_KEY`
- Value: Your Gemini API key from Step 1

### Step 6: Test Your Automation

1. Go to the "Actions" tab in your repository
2. Click "Facebook News Automation" in the left sidebar
3. Click "Run workflow" → "Run workflow"
4. Wait about 1 minute
5. Click on the workflow run to see the results
6. Check your Facebook page for the post!

---

## ⏰ Schedule Configuration

The automation runs **every 6 hours** by default. To change this:

1. Edit `.github/workflows/facebook_automation.yml`
2. Find the `cron:` line
3. Change to your preferred schedule:

```yaml
# Every 6 hours (default)
- cron: '0 */6 * * *'

# Every 4 hours
- cron: '0 */4 * * *'

# Three times a day (9 AM, 3 PM, 9 PM UTC)
- cron: '0 9,15,21 * * *'

# Once daily at 9 AM UTC
- cron: '0 9 * * *'

# Twice daily (8 AM and 6 PM UTC)
- cron: '0 8,18 * * *'
```

**Note:** Times are in UTC. To convert to your local time, check: https://www.worldtimebuddy.com/

---

## 📰 Customizing News Sources

To change which Spanish news sites are monitored:

1. Edit `facebook_automation.py`
2. Find the `NEWS_FEEDS` list
3. Add or remove RSS feed URLs

**Popular Spanish News RSS Feeds:**
```python
NEWS_FEEDS = [
    # Spanish National News
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
    'https://rss.elmundo.es/rss/mundo.xml',
    
    # Latin America
    'https://www.clarin.com/rss/lo-ultimo/',  # Argentina
    'https://www.eluniversal.com.mx/rss.xml',  # Mexico
    
    # Business
    'https://cincodias.elpais.com/rss/cincodias/portada.xml',
    
    # Tech
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada',
]
```

---

## 🎨 Customizing Content Mix

The bot posts different types of content based on weighted probabilities. To adjust the mix:

1. Edit `facebook_automation.py`
2. Find the `CONTENT_TYPES` dictionary
3. Adjust the percentages (must total 100):

```python
CONTENT_TYPES = {
    'news': 50,      # 50% - Translated Spanish news
    'quito': 30,     # 30% - Quito stories and tips
    'meme': 20,      # 20% - Expat memes
}
```

**Examples:**
- More news-focused: `{'news': 70, 'quito': 20, 'meme': 10}`
- More fun/engaging: `{'news': 30, 'quito': 30, 'meme': 40}`
- News only: `{'news': 100, 'quito': 0, 'meme': 0}`

---

## 📸 Adding Quito Photos (Optional)

To post beautiful photos of Quito with your content:

1. Get a free Unsplash API key: https://unsplash.com/developers
2. Add it as a GitHub secret: `UNSPLASH_API_KEY`
3. Photos will automatically appear with Quito content

Without this key, Quito posts will still work (just text-only).

---

## 🎨 Customizing Post Style

To change how posts are formatted, edit the `prompt` in `facebook_automation.py`:

```python
prompt = f"""
You are helping create engaging Facebook posts for an expat community page. 

Translate this Spanish news article to English and create a Facebook post that:
- Translates the key information accurately
- Makes it relevant and interesting for expats
- Keeps it concise (2-3 sentences)
- Uses a friendly, conversational tone
- Includes relevant emoji
- Includes the original source link at the end

[YOUR CUSTOM INSTRUCTIONS HERE]
"""
```

---

## 🔍 Troubleshooting

### "Error posting to Facebook"
- Check your access token hasn't expired (renew every 60 days)
- Verify page permissions in Facebook Developer Console
- Make sure secrets are correctly added in GitHub

### "Error with Gemini API"
- Check your API key is correct
- Verify you haven't exceeded free tier limits
- Check Gemini API status: https://status.cloud.google.com/

### "No articles found"
- RSS feeds might be down temporarily
- Try different news sources
- Check internet connectivity in the GitHub Action logs

### Posts aren't appearing
- Check the Actions tab for error logs
- Verify the schedule is set correctly
- Manually trigger a test run

---

## 💡 Pro Tips

1. **Access Token Renewal:** Set a calendar reminder for 50 days to renew your Facebook access token

2. **Test First:** Always use "Run workflow" manually before relying on the schedule

3. **Monitor Limits:**
   - Gemini Free Tier: 60 requests/minute
   - GitHub Actions Free Tier: 2,000 minutes/month (plenty for this)

4. **Content Variety Works:** The mix of news, local content, and humor keeps followers engaged

5. **Customize Topics:** Edit the topic lists in `generate_quito_content()` and `generate_expat_meme()` to match your audience

6. **Peak Posting Times:** Adjust the schedule to post when your audience is most active

7. **Engagement:** The AI generates questions at the end of posts - respond to comments to build community

8. **Add Your Voice:** You can edit posts manually after they're published to add personal touches

---

## 📊 Next Steps & Enhancements

Once running smoothly, you can:

1. **Add images** - Fetch article images and post them with the text
2. **Track analytics** - Log which posts perform best
3. **Filter topics** - Only post about specific subjects (politics, economy, etc.)
4. **Multiple languages** - Translate to other languages for different audiences
5. **Engagement replies** - Auto-respond to comments (advanced)

---

## 🆘 Need Help?

- GitHub Actions docs: https://docs.github.com/en/actions
- Facebook Graph API docs: https://developers.facebook.com/docs/graph-api
- Gemini API docs: https://ai.google.dev/docs

---

## 📝 License

Free to use and modify for your own projects!
