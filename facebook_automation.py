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
from dotenv import load_dotenv
import re

# Load variables from .env file automatically
load_dotenv()

# Debug: Check if .env loaded
print("🔍 Debug: Checking environment variables...")
print(f"   .env file exists in current directory: {os.path.exists('.env')}")

# Configuration from environment variables
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')

# Debug output
print(f"   FACEBOOK_PAGE_ID loaded: {'✓' if FACEBOOK_PAGE_ID else '✗'} ({FACEBOOK_PAGE_ID[:10] + '...' if FACEBOOK_PAGE_ID else 'None'})")
print(f"   FACEBOOK_ACCESS_TOKEN loaded: {'✓' if FACEBOOK_ACCESS_TOKEN else '✗'} ({FACEBOOK_ACCESS_TOKEN[:10] + '...' if FACEBOOK_ACCESS_TOKEN else 'None'})")
print(f"   GEMINI_API_KEY loaded: {'✓' if GEMINI_API_KEY else '✗'} ({GEMINI_API_KEY[:10] + '...' if GEMINI_API_KEY else 'None'})")
print(f"   UNSPLASH_API_KEY loaded: {'✓' if UNSPLASH_API_KEY else '✗'} ({UNSPLASH_API_KEY[:10] + '...' if UNSPLASH_API_KEY else 'None'})")
print()

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

def clean_ai_response(text):
    """Remove common AI preambles and clean up the response"""
    
    # Common preambles to remove
    preambles = [
        r"^here'?s?\s+an?\s+engaging\s+facebook\s+post.*?:",
        r"^here'?s?\s+a\s+facebook\s+post.*?:",
        r"^here'?s?\s+the\s+post.*?:",
        r"^here'?s?\s+a\s+.*?post.*?:",
        r"^here'?s?\s+the\s+.*?post.*?:",
        r"^facebook\s+post.*?:",
        r"^post.*?:",
    ]
    
    cleaned = text.strip()
    
    # Remove preambles (case insensitive)
    for preamble in preambles:
        cleaned = re.sub(preamble, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove leading/trailing whitespace and newlines
    cleaned = cleaned.strip()
    
    # Remove markdown code blocks if present
    cleaned = re.sub(r'^```.*?\n', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'\n```$', '', cleaned, flags=re.MULTILINE)
    
    return cleaned

def search_relevant_image(query, orientation='landscape'):
    """Search for a relevant image using Unsplash API"""
    
    if not UNSPLASH_API_KEY:
        return None
    
    try:
        url = "https://api.unsplash.com/photos/random"
        params = {
            'query': query,
            'client_id': UNSPLASH_API_KEY,
            'orientation': orientation
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'url': data['urls']['regular'],
            'credit': f"📸 {data['user']['name']} on Unsplash",
            'download_url': data['links']['download_location']
        }
    except Exception as e:
        print(f"⚠️ Could not fetch image: {e}")
        return None

def generate_quito_content():
    """Generate interesting Quito content using Gemini"""
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
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
    
    prompt = f"""Write a natural, conversational Facebook post about: {topic}

CRITICAL INSTRUCTIONS:
- DO NOT include any preamble like "Here's a post" or similar
- Start directly with the post content
- Write 3-4 sentences maximum
- Sound like a real person sharing helpful local knowledge, not an AI
- Include 1-2 relevant emojis naturally in the text
- End with an engaging question to encourage comments
- Be specific and actionable
- Use a warm, friendly tone

Write only the post text, nothing else:"""
    
    try:
        response = model.generate_content(prompt)
        cleaned_text = clean_ai_response(response.text)
        
        # Search for a relevant Quito image
        image_keywords = ['quito ecuador', 'quito city', 'ecuador', 'quito architecture']
        image = search_relevant_image(random.choice(image_keywords))
        
        if image:
            cleaned_text += f"\n\n{image['credit']}"
            return cleaned_text, image['url']
        else:
            return cleaned_text, None
            
    except Exception as e:
        print(f"Error generating Quito content: {e}")
        return None, None

def generate_expat_meme():
    """Generate expat meme content using Gemini"""
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
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
    
    prompt = f"""Write a funny, relatable Facebook post for expats in Ecuador about: {theme}

CRITICAL INSTRUCTIONS:
- DO NOT include any preamble like "Here's a post" or similar
- Start directly with the post content
- Keep it very short (2-3 sentences max)
- Sound like a real expat sharing a funny moment, not an AI
- Use emojis naturally and appropriately
- Be lighthearted and relatable, never mean-spirited
- End with something like "Can you relate? 😂" or "Tell me I'm not alone 🤣"

Write only the post text, nothing else:"""
    
    try:
        response = model.generate_content(prompt)
        cleaned_text = clean_ai_response(response.text)
        
        # Try to find a humorous/relatable image
        image_queries = ['ecuador culture', 'quito daily life', 'latin america expat', 'ecuador street']
        image = search_relevant_image(random.choice(image_queries))
        
        if image:
            cleaned_text += f"\n\n{image['credit']}"
            return cleaned_text, image['url']
        else:
            return cleaned_text, None
            
    except Exception as e:
        print(f"Error generating meme content: {e}")
        return None, None

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
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Translate this Spanish news article to English and create a natural Facebook post.

CRITICAL INSTRUCTIONS:
- DO NOT include any preamble like "Here's a post" or similar
- Start directly with the post content
- Write like a real person sharing interesting news, not an AI
- Keep it concise (2-3 sentences that capture the key story)
- Use a conversational, engaging tone
- Include 1-2 relevant emojis naturally
- Make it relevant to expats living in Ecuador/Latin America
- End with the source link EXACTLY like this format: "Read more: [URL]"

Spanish Article:
Title: {article['title']}
Content: {article['summary'][:500]}
Source: {article['link']}

Write only the Facebook post text (no preamble, no markdown):"""
    
    try:
        response = model.generate_content(prompt)
        cleaned_text = clean_ai_response(response.text)
        
        # Ensure the link is included
        if article['link'] not in cleaned_text:
            cleaned_text += f"\n\nRead more: {article['link']}"
        
        # Try to find a relevant news image
        # Extract key topics from title for image search
        image_keywords = extract_image_keywords(article['title'])
        image = search_relevant_image(image_keywords)
        
        return cleaned_text, image['url'] if image else None
        
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback to simple format
        fallback = f"📰 {article['title']}\n\n{article['summary'][:200]}...\n\nRead more: {article['link']}"
        return fallback, None

def extract_image_keywords(title):
    """Extract relevant keywords from news title for image search"""
    # Remove common words and keep important ones
    common_words = ['el', 'la', 'los', 'las', 'de', 'del', 'en', 'y', 'a', 'con', 'por', 'para', 'un', 'una']
    words = title.lower().split()
    keywords = [w for w in words if w not in common_words and len(w) > 3]
    
    # Take first 2-3 meaningful keywords
    search_query = ' '.join(keywords[:3]) if keywords else 'spain news'
    return search_query

def post_to_facebook(message, image_url=None):
    """Post message to Facebook page, optionally with an image"""
    
    if image_url:
        url = f"https://graph.facebook.com/v21.0/{FACEBOOK_PAGE_ID}/photos"
        payload = {
            'message': message,
            'url': image_url,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
    else:
        url = f"https://graph.facebook.com/v21.0/{FACEBOOK_PAGE_ID}/feed"
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
            print(f"📄 Processing: {article['title'][:60]}...")
            print("🤖 Translating with Gemini...")
            post_content, image_url = translate_and_summarize_with_gemini(article)
    
    if content_type == 'quito':
        # Generate Quito content
        print("🏔️ Generating Quito content...")
        post_content, image_url = generate_quito_content()
    
    if content_type == 'meme':
        # Generate expat meme
        print("😂 Generating expat meme content...")
        post_content, image_url = generate_expat_meme()
    
    if not post_content:
        print("❌ Failed to generate content")
        return
    
    print(f"\n📄 Generated post:")
    print("="*60)
    print(post_content)
    print("="*60)
    if image_url:
        print(f"🖼️ Image URL: {image_url[:60]}...")
    print()
    
    # Post to Facebook
    print("📤 Posting to Facebook...")
    success = post_to_facebook(post_content, image_url)
    
    if success:
        print(f"\n✅ Automation complete! Posted: {content_type}")
        if image_url:
            print("📸 Posted with image!")
    else:
        print(f"\n❌ Post failed")

if __name__ == "__main__":
    main()
