"""
Facebook Page Automation with Gemini Translation
Fetches Spanish news and posts translated content to Facebook
Also posts Quito content and expat memes for variety
"""

import os
import requests
import json
from datetime import datetime
import feedparser
import google.generativeai as genai
import random

# Configuration from environment variables
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Spanish news RSS feeds (you can customize these)
NEWS_FEEDS = [
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
    'https://rss.elmundo.es/rss/mundo.xml',
    'https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml',
]

# Content types and their weights (probability of posting each type)
CONTENT_TYPES = {
    'news': 50,      # 50% chance - translated news
    'quito': 30,     # 30% chance - Quito stories/photos
    'meme': 20,      # 20% chance - expat memes
}

def generate_quito_content():
    """Generate interesting Quito content using Gemini"""
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    quito_topics = [
        "hidden gems and secret spots in Quito that expats should know about",
        "best neighborhoods in Quito for expats and what makes them special",
        "traditional Ecuadorian food you must try in Quito",
        "day trips from Quito - nearby attractions and how to get there",
        "cost of living tips for expats in Quito",
        "cultural differences expats notice when living in Quito",
        "best cafes and coworking spaces in Quito",
        "weekend activities and things to do in Quito",
        "navigating Quito's transportation system as an expat",
        "learning Spanish in Quito - tips and resources",
        "Quito's weather and what to pack for each season",
        "making friends as an expat in Quito",
        "beautiful viewpoints and photo spots in Quito",
        "festivals and cultural events in Quito",
        "expat-friendly doctors and services in Quito"
    ]
    
    topic = random.choice(quito_topics)
    
    prompt = f"""
Create an engaging Facebook post for an expat community page about: {topic}

Requirements:
- Write 3-4 sentences
- Make it helpful, interesting, and actionable
- Use a friendly, conversational tone
- Include 1-2 relevant emojis
- End with a question to encourage engagement

Create the post:
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip(), 'text'
    except Exception as e:
        print(f"Error generating Quito content: {e}")
        return None, None

def generate_expat_meme():
    """Generate expat meme content using Gemini"""
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    meme_themes = [
        "explaining to family back home what life in Ecuador is like",
        "the difference between tourist prices and local prices",
        "trying to understand Ecuadorian Spanish slang",
        "dealing with altitude in Quito for the first time",
        "when you finally understand a joke in Spanish",
        "expat budget vs reality in Ecuador",
        "missing food from home vs discovering amazing local food",
        "learning to navigate Quito traffic",
        "when locals speak too fast in Spanish",
        "adjusting to Ecuador time vs your home country time",
        "trying to explain American portions vs Ecuadorian portions",
        "the face you make when you understand Spanish news",
        "realizing everything closes during siesta",
        "expat WhatsApp groups be like",
        "when you start preferring ecuadorian food over your home country food"
    ]
    
    theme = random.choice(meme_themes)
    
    prompt = f"""
Create a funny, relatable Facebook post for expats living in Ecuador/Quito about: {theme}

Requirements:
- Make it humorous and relatable
- Keep it short (2-3 sentences max)
- Use emojis appropriately
- Be lighthearted and fun, never mean-spirited
- Include a call-to-action like "Can anyone relate? 😂" or "Drop a 😂 if this is you"

Create the funny post:
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip(), 'text'
    except Exception as e:
        print(f"Error generating meme content: {e}")
        return None, None

def search_quito_image():
    """Search for a beautiful Quito image using Unsplash API"""
    
    # Unsplash provides free images
    # If you want to add images, get a free API key from https://unsplash.com/developers
    unsplash_key = os.environ.get('UNSPLASH_API_KEY')
    
    if not unsplash_key:
        return None
    
    try:
        keywords = ['quito ecuador', 'quito city', 'quito architecture', 'ecuador landscape']
        keyword = random.choice(keywords)
        
        url = f"https://api.unsplash.com/photos/random"
        params = {
            'query': keyword,
            'client_id': unsplash_key,
            'orientation': 'landscape'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'url': data['urls']['regular'],
            'credit': f"📸 Photo by {data['user']['name']} on Unsplash",
            'download_url': data['links']['download_location']
        }
    except Exception as e:
        print(f"Error fetching Quito image: {e}")
        return None

def choose_content_type():
    """Randomly choose content type based on weights"""
    content_list = []
    for content_type, weight in CONTENT_TYPES.items():
        content_list.extend([content_type] * weight)
    
    return random.choice(content_list)

def fetch_latest_news(max_articles=5):
    """Fetch latest articles from Spanish news feeds"""
    articles = []
    
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:2]:  # Get 2 from each feed
                articles.append({
                    'title': entry.title,
                    'summary': entry.get('summary', entry.get('description', '')),
                    'link': entry.link,
                    'published': entry.get('published', '')
                })
                if len(articles) >= max_articles:
                    break
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
        
        if len(articles) >= max_articles:
            break
    
    return articles

def translate_and_summarize_with_gemini(article):
    """Use Gemini to translate and create engaging post content"""
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""
You are helping create engaging Facebook posts for an expat community page. 

Translate this Spanish news article to English and create a Facebook post that:
- Translates the key information accurately
- Makes it relevant and interesting for expats
- Keeps it concise (2-3 sentences)
- Uses a friendly, conversational tone
- Includes the original source link at the end

Spanish Article:
Title: {article['title']}
Summary: {article['summary']}
Link: {article['link']}

Create an engaging Facebook post in English:
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback to simple translation
        return f"📰 {article['title']}\n\n{article['summary'][:200]}...\n\nRead more: {article['link']}"

def post_to_facebook(message, image_url=None):
    """Post message to Facebook page, optionally with an image"""
    
    if image_url:
        # Post with image
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
        payload = {
            'message': message,
            'url': image_url,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
    else:
        # Text-only post
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
        payload = {
            'message': message,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Successfully posted to Facebook! Post ID: {result.get('id') or result.get('post_id')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to Facebook: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main automation workflow"""
    
    print(f"🤖 Starting Facebook automation - {datetime.now()}")
    
    # Validate environment variables
    if not all([FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN, GEMINI_API_KEY]):
        print("❌ Missing required environment variables!")
        print(f"FACEBOOK_PAGE_ID: {'✓' if FACEBOOK_PAGE_ID else '✗'}")
        print(f"FACEBOOK_ACCESS_TOKEN: {'✓' if FACEBOOK_ACCESS_TOKEN else '✗'}")
        print(f"GEMINI_API_KEY: {'✓' if GEMINI_API_KEY else '✗'}")
        return
    
    # Choose what type of content to post
    content_type = choose_content_type()
    print(f"📝 Selected content type: {content_type}")
    
    post_content = None
    image_url = None
    
    if content_type == 'news':
        # Fetch and translate news
        print("📰 Fetching latest Spanish news...")
        articles = fetch_latest_news(max_articles=3)
        
        if not articles:
            print("❌ No articles found, falling back to Quito content")
            content_type = 'quito'
        else:
            article = articles[0]
            print(f"📝 Processing: {article['title'][:50]}...")
            print("🤖 Translating with Gemini...")
            post_content = translate_and_summarize_with_gemini(article)
    
    if content_type == 'quito':
        # Generate Quito content
        print("🏔️ Generating Quito content...")
        post_content, content_format = generate_quito_content()
        
        # Try to add a Quito image (optional)
        quito_image = search_quito_image()
        if quito_image:
            image_url = quito_image['url']
            post_content += f"\n\n{quito_image['credit']}"
            print(f"📸 Found Quito image!")
    
    if content_type == 'meme':
        # Generate expat meme
        print("😂 Generating expat meme content...")
        post_content, content_format = generate_expat_meme()
    
    if not post_content:
        print("❌ Failed to generate content")
        return
    
    print(f"\n📄 Generated post:\n{post_content}\n")
    
    # Post to Facebook
    print("📤 Posting to Facebook...")
    post_to_facebook(post_content, image_url)
    
    print(f"\n✅ Automation complete! Posted: {content_type}")

if __name__ == "__main__":
    main()
