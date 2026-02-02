# 🤖 Facebook Expat News Automation

Automatically translate Spanish news and post to your Facebook page using AI.

## ✨ Features

- 🌍 Fetches latest Spanish news from multiple sources
- 🤖 AI-powered translation using Google Gemini 2.5
- 🏔️ AI-generated Quito stories, tips, and local content
- 😂 Funny expat memes and relatable content
- 📱 Automatic posting to Facebook page with smart content mixing
- 📸 Optional beautiful Quito photos (via Unsplash API)
- ⏰ Runs on schedule (every 6 hours by default)
- 💯 Completely FREE using GitHub Actions

## 🎯 Content Mix

- **50% News** - Translated Spanish news relevant to expats
- **30% Quito Content** - Local tips, hidden gems, cultural insights
- **20% Memes** - Relatable expat humor

(Fully customizable percentages)

## 🚀 Quick Start

1. Read the **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for complete instructions
2. Get your API keys (Facebook, Gemini)
3. Add secrets to GitHub repository
4. Let it run automatically!

## 📅 Schedule

Posts are published every 6 hours. Customize in `.github/workflows/facebook_automation.yml`

## 🛠️ Customization

- **Content mix**: Edit `CONTENT_TYPES` percentages in `facebook_automation.py`
- **News sources**: Edit `NEWS_FEEDS` list
- **Quito topics**: Customize topics in `generate_quito_content()`
- **Meme themes**: Customize themes in `generate_expat_meme()`
- **Post style**: Modify the Gemini prompts
- **Frequency**: Change the cron schedule
- **Add photos**: Get free Unsplash API key for Quito images

## 📖 Full Documentation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions and troubleshooting.

---

**Made for expat communities 🌎**
