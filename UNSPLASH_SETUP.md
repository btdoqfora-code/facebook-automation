# 📸 Adding Images to Your Posts - Unsplash Setup

## Why Add Images?

Posts with images get **2-3x more engagement** than text-only posts. This update adds professional, relevant images to ALL your posts automatically!

## Quick Setup (5 minutes)

### Step 1: Get Your Free Unsplash API Key

1. Go to: **https://unsplash.com/developers**

2. Click **"Register as a Developer"** (it's free!)

3. Accept the terms and create account (or log in if you have one)

4. Click **"New Application"**

5. Fill in the form:
   - **Application name**: "Facebook Automation Bot"
   - **Description**: "Automated Facebook posting with curated images"
   - Accept the terms ✓

6. Click **"Create Application"**

7. You'll see your keys:
   - **Access Key** ← This is what you need!
   - Secret Key (you don't need this)

8. Copy your **Access Key** (it looks like: `abc123xyz789...`)

### Step 2: Add to GitHub Secrets

1. Go to your GitHub repository

2. Click **Settings** → **Secrets and variables** → **Actions**

3. Click **"New repository secret"**

4. Add the secret:
   - **Name**: `UNSPLASH_API_KEY`
   - **Value**: Paste your Access Key from step 1
   - Click **"Add secret"**

### Step 3: Test It!

1. Go to **Actions** tab in your repo

2. Click **"Facebook News Automation"**

3. Click **"Run workflow"** → **"Run workflow"**

4. Wait ~1 minute

5. Check your Facebook page - your post should now have a beautiful image! 📸

## What You'll Get

### News Posts
- Relevant images based on article topic
- Example: Spain politics article → Spanish landmark image

### Quito Content
- Beautiful photos of Quito, Ecuador
- Local scenes, architecture, landscapes

### Expat Memes
- Relatable, fun images
- Cultural and lifestyle photos

### All Posts Include
- Professional quality images
- Proper attribution: "📸 Photographer Name on Unsplash"
- Relevant to the content

## Unsplash Free Tier Limits

- **50 requests per hour**
- **5,000 requests per month**

**Your usage**: ~4-8 posts per day = ~240 requests/month

✅ You're well within the free limits!

## Troubleshooting

### "Images not appearing in my posts"

**Check these:**

1. ✓ UNSPLASH_API_KEY is added to GitHub secrets
2. ✓ Key is spelled exactly: `UNSPLASH_API_KEY`
3. ✓ You copied the Access Key (not Secret Key)
4. ✓ You re-ran the workflow after adding the secret

### "Rate limit exceeded"

This means you've used your 50 requests in an hour. Solutions:

1. **Wait 1 hour** - limits reset hourly
2. **Reduce posting frequency** - Post every 8 hours instead of 6
3. **Upgrade Unsplash** - Get more requests (optional, paid)

### "Images don't match content"

The bot searches for relevant keywords. To improve:

1. Edit `extract_image_keywords()` in the Python file
2. Add more specific search terms
3. Adjust the keyword extraction logic

## Optional: Improve Image Relevance

Want better image matching? Edit the search queries:

```python
# In facebook_automation.py

# For news posts - edit extract_image_keywords()
def extract_image_keywords(title):
    # Add your own logic here
    # Example: detect "Spain" in title → search "spain landmarks"
    pass

# For Quito posts - edit the keywords list
image_keywords = [
    'quito ecuador',
    'quito city sunset',  # Add specific searches
    'ecuador andes mountains',
]

# For meme posts - edit the queries
image_queries = [
    'ecuador culture',
    'latin america street',
    'coffee shop coworking',  # More specific
]
```

## Upgrading to Paid (Optional)

If you post very frequently:

1. Go to: https://unsplash.com/developers
2. Click your app
3. Click "Request Production"
4. Fill in the form (why you need more requests)
5. Get approved for 5,000 requests/hour

**Cost**: FREE! Unsplash approves most apps quickly.

## Alternative: Use Without Images

If you don't want to add images:

1. Simply **don't add** the `UNSPLASH_API_KEY` secret
2. The bot will work perfectly fine
3. Posts will be text-only (still great content!)

The code is designed to work with or without images.

## Best Practices

### DO:
- ✅ Keep photo credits in posts (required by Unsplash)
- ✅ Use relevant search keywords
- ✅ Stay within rate limits
- ✅ Review posts occasionally to ensure image quality

### DON'T:
- ❌ Remove photo credits (violates Unsplash terms)
- ❌ Use images for commercial purposes without proper plan
- ❌ Hotlink images (the bot downloads via API, which is correct)

## Example Before/After

### BEFORE (Without Images)
```
📰 Spain approves new housing measures for 2024...

Read more: https://elpais.com/...
```

**Engagement**: 👍 5-10 reactions

### AFTER (With Images)
```
📰 Spain approves new housing measures for 2024...

Read more: https://elpais.com/...

[Beautiful image of Spanish architecture]
📸 Maria García on Unsplash
```

**Engagement**: 👍 20-30 reactions, 💬 5-10 comments

## Summary Checklist

- [ ] Create Unsplash developer account
- [ ] Create new application
- [ ] Copy Access Key
- [ ] Add `UNSPLASH_API_KEY` to GitHub secrets
- [ ] Test the workflow
- [ ] Check Facebook page for images
- [ ] Enjoy better engagement! 🎉

---

**Questions?** Check the main README.md or create an issue on GitHub!

**Happy posting! 📸✨**
