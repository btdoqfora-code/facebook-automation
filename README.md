# 🤖 Facebook Expat News Automation

Automatically translate Spanish news and post to your Facebook page using AI - with beautiful images!

## ✨ Features

- 🌍 Fetches latest Spanish news from multiple sources
- 🤖 AI-powered translation using Google Gemini 2.5
- 🏔️ AI-generated Quito stories, tips, and local content
- 😂 Funny expat memes and relatable content
- 📸 **NEW: Automatic relevant images for ALL posts** (via Unsplash)
- 🔗 **NEW: Proper source links included in all news posts**
- 👤 **NEW: More human-like, natural writing** (no AI preambles)
- 📱 Automatic posting to Facebook page with smart content mixing
- ⏰ Runs on schedule (every 6 hours by default)
- 💯 Completely FREE using GitHub Actions

## 🎯 Content Mix

- **50% News** - Translated Spanish news relevant to expats (with images & links)
- **30% Quito Content** - Local tips, hidden gems, cultural insights (with photos)
- **20% Memes** - Relatable expat humor (with images)

(Fully customizable percentages)

## 🚀 Quick Start

1. **Get API Keys** (all free!):
   - Facebook Page ID & Access Token
   - Google Gemini API key
   - **Unsplash API key** (for images)

2. **Setup GitHub Repository**:
   - Create new repo
   - Upload files
   - Add 4 secrets (including UNSPLASH_API_KEY)

3. **Run & Enjoy**:
   - Test manually first
   - Let it run automatically every 6 hours
   - Watch engagement grow! 📈

## 🎨 What's New in This Version

### Better Post Quality
- ✅ No more "Here's an engaging post..." preambles
- ✅ Natural, human-like writing
- ✅ Proper formatting and emojis

### Images Everywhere
- ✅ News posts get relevant images
- ✅ Quito content gets beautiful city photos
- ✅ Meme posts get relatable images
- ✅ All images credited properly

### Better Links
- ✅ News articles always link to source
- ✅ "Read more:" format is clean and professional
- ✅ Links are properly embedded in posts

## 📋 Setup Instructions

### Step 1: Get Unsplash API Key (NEW!)

1. Go to: https://unsplash.com/developers
2. Click "Register as a Developer"
3. Create a new app
4. Copy your "Access Key"
5. Save it - you'll add it to GitHub secrets

**Why Unsplash?**
- Completely free
- High-quality, professional images
- Relevant search results
- Legal to use with attribution

### Step 2: Get Other API Keys

**Facebook:**
- Page ID: From your page URL
- Access Token: From Facebook Developer Console
  - Get a long-lived token (60 days)
  - Needs: `pages_manage_posts`, `pages_read_engagement`

**Gemini:**
- Go to: https://makersuite.google.com/app/apikey
- Create API key
- Free tier: 60 requests/minute (plenty!)

### Step 3: Setup GitHub

1. Create new repository (public for free Actions)
2. Upload these files:
   - `facebook_automation.py`
   - `requirements.txt`
   - `.github/workflows/facebook_automation.yml`

3. Add GitHub Secrets (Settings → Secrets → Actions):
   - `FACEBOOK_PAGE_ID`
   - `FACEBOOK_ACCESS_TOKEN`
   - `GEMINI_API_KEY`
   - `UNSPLASH_API_KEY` ⭐ **NEW!**

### Step 4: Test It!

1. Go to Actions tab
2. Click "Facebook News Automation"
3. Click "Run workflow"
4. Check your Facebook page in ~1 minute!

## 🎨 Example Posts

**News Post:**
```
📰 Spain's new pension reform is making waves! The government just approved 
anti-eviction measures for property owners, allowing more flexibility for those 
renting. This could be great news for expats considering long-term stays. 💰

Read more: https://elpais.com/...

[Beautiful relevant image]
📸 Maria García on Unsplash
```

**Quito Content:**
```
The best hidden cafes in La Floresta are absolute gems! ☕ La Cleta and Café 
Mosaico offer amazing views, great wifi, and the perfect spot for digital nomads. 
Plus, you'll pay half what you would in tourist areas. 

What's your favorite local spot? 🏔️

[Photo of Quito cafe]
📸 Juan Lopez on Unsplash
```

**Expat Meme:**
```
That moment when you finally understand a joke in Spanish without translating 
it in your head first 🤯 Peak expat achievement unlocked! 

Tell me I'm not alone 🤣

[Relatable image]
📸 Alex Rivera on Unsplash
```

## ⚙️ Customization

### Adjust Content Mix

Edit `CONTENT_TYPES` in `facebook_automation.py`:
```python
CONTENT_TYPES = {
    'news': 50,      # More news
    'quito': 30,     # More local content
    'meme': 20,      # More humor
}
```

### Change Posting Schedule

Edit `.github/workflows/facebook_automation.yml`:
```yaml
# Every 4 hours
- cron: '0 */4 * * *'

# Three times daily
- cron: '0 9,15,21 * * *'
```

### Add News Sources

Edit `NEWS_FEEDS` list:
```python
NEWS_FEEDS = [
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
    'https://www.clarin.com/rss/lo-ultimo/',  # Argentina
    'https://www.eluniversal.com.mx/rss.xml',  # Mexico
]
```

### Customize Topics

Edit topic lists in:
- `generate_quito_content()` - Add your own Quito topics
- `generate_expat_meme()` - Add your own meme themes

## 🔧 Troubleshooting

### Images Not Appearing?
- Check your Unsplash API key is correct
- Verify it's added to GitHub secrets
- Free tier: 50 requests/hour (plenty for 4 posts/day)

### "Here's a post..." Still Showing?
- This version fixes that!
- The `clean_ai_response()` function removes AI preambles
- If it still happens, the cleaning function will catch it

### Links Not Working?
- Check the article RSS feed has URLs
- The code now forces links to be included
- Format: "Read more: [URL]"

### Need Better Images?
- Upgrade Unsplash plan for more requests
- Or use specific keywords in search queries
- Edit `extract_image_keywords()` function

## 💡 Pro Tips

1. **Image Quality**: Unsplash images are professional-grade - your posts will look amazing!

2. **Engagement**: Posts with images get 2-3x more engagement than text-only

3. **Credits**: Always keep the photo credits - it's required by Unsplash and looks professional

4. **Testing**: Run manually 3-4 times to see the variety of content

5. **Timing**: Schedule posts for when your audience is most active

6. **Monitor**: Check which content type performs best and adjust ratios

7. **Personalize**: After posts go live, add your own comment to start conversations

## 📊 Expected Results

- **Higher Engagement**: Images boost clicks and comments
- **More Professional**: Clean formatting without AI tells
- **Better Trust**: Source links show credibility
- **Variety**: Different content types keep feed interesting

## 🆘 Support

- Full setup guide: `SETUP_GUIDE.md`
- GitHub Actions docs: https://docs.github.com/en/actions
- Unsplash API docs: https://unsplash.com/documentation
- Facebook Graph API: https://developers.facebook.com/docs/graph-api

## 📝 What Changed From Previous Version

✅ Added `clean_ai_response()` function to remove AI preambles
✅ Integrated Unsplash API for all content types
✅ Improved prompts to sound more human
✅ Better link formatting in news posts
✅ Image credit attribution
✅ Keyword extraction for relevant news images
✅ Better error handling for images

---

**Made with ❤️ for expat communities 🌎**

Now with images and proper links! 📸🔗
