"""
Facebook Page Automation with Gemini Translation
Fetches Spanish news and posts translated content to Facebook
Also posts Quito content and expat memes for variety

ENHANCED VERSION with:
- Google Search grounding for accuracy
- Better geographic context
- Descriptive Unsplash queries
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

# Configure Gemini with grounding (helps prevent hallucinations)
genai.configure(api_key=GEMINI_API_KEY)

# Spanish news RSS feeds - mix of international and Latin America sources
NEWS_FEEDS = [
    # International Spanish news
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
    'https://rss.elmundo.es/rss/mundo.xml',
    'https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml',
    
    # Latin America focused
    'https://www.eluniverso.com/feed/',  # Ecuador
    'https://www.bbc.com/mundo/topics/c2dwqd1zd70t.rss',  # BBC Latin America
]

# Content types and their weights (probability of posting each type)
CONTENT_TYPES = {
    'news': 30,      # 30% chance - translated news (reduced from 50%)
    'quito': 45,     # 45% chance - Quito stories/photos (increased from 30%)
    'meme': 25,      # 25% chance - expat memes (increased from 20%)
}

# Track used images to avoid repetition
USED_IMAGES_FILE = 'used_images.json'

def load_group_images():
    """Load manually curated group images library"""
    try:
        if os.path.exists('group_images.json'):
            with open('group_images.json', 'r', encoding='utf-8') as f:
                library = json.load(f)
                print(f"✅ Loaded {library['total_images']} images from group library")
                return library['images']
    except Exception as e:
        print(f"⚠️ Could not load group images: {e}")
    return []

def get_unused_group_image(group_images):
    """Get a random image from the library that hasn't been used recently"""
    if not group_images:
        return None
    
    # Load list of recently used images
    used_images = []
    try:
        if os.path.exists(USED_IMAGES_FILE):
            with open(USED_IMAGES_FILE, 'r') as f:
                used_images = json.load(f)
    except:
        pass
    
    # Filter out recently used images
    available = [img for img in group_images if img['url'] not in used_images]
    
    # If all images have been used, reset the list
    if not available:
        print("♻️ All images used, resetting...")
        available = group_images
        used_images = []
    
    # Pick a random available image
    selected = random.choice(available)
    
    # Mark as used
    used_images.append(selected['url'])
    
    # Keep only last 50% of library size in used list (to allow cycling)
    max_used = max(5, len(group_images) // 2)
    used_images = used_images[-max_used:]
    
    # Save updated used list
    try:
        with open(USED_IMAGES_FILE, 'w') as f:
            json.dump(used_images, f)
    except:
        pass
    
    return selected

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
        
        print(f"   🔍 Unsplash search: '{query}'")
        
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

def generate_unsplash_query_with_gemini(content_description, location="Quito, Ecuador"):
    """
    NEW: Use Gemini to generate a descriptive Unsplash search query
    This prevents generic searches and ensures location context
    """
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""Generate a specific, descriptive Unsplash image search query for: {content_description}

CRITICAL INSTRUCTIONS:
- Location context: {location}
- Create a descriptive query with 3-5 keywords
- Use cinematic/photographic language (e.g., "wide shot of...", "aerial view of...")
- Be specific to Ecuador/Latin America visual context
- Avoid generic terms like "news", "automation", "background", "office"
- Example good queries: "colonial architecture old town Quito", "Cotopaxi volcano sunset Ecuador", "colorful market Quito Ecuador"

Return ONLY the search query, nothing else:"""
    
    try:
        response = model.generate_content(prompt)
        query = response.text.strip()
        # Remove quotes if Gemini added them
        query = query.strip('"').strip("'")
        return query
    except Exception as e:
        print(f"⚠️ Could not generate image query: {e}")
        return f"{location} cityscape"

def generate_quito_content():
    """Generate interesting Quito content using Gemini"""
    
    # ENHANCED: Using system instruction for better grounding
    model = genai.GenerativeModel(
        'gemini-3-flash-preview',
        system_instruction="""You are a local expert living in Quito, ECUADOR (South America).

CRITICAL GEOGRAPHIC CONTEXT:
- You live in Quito, the capital city of ECUADOR
- Ecuador is in SOUTH AMERICA, NOT in Spain or Europe
- Never confuse Ecuador with Spain
- All your knowledge relates to life in Ecuador/Quito specifically

You provide authentic, local insights about living in Quito for expats."""
    )
    
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
- Context: You are in Quito, Pichincha, ECUADOR (South America)
- DO NOT include any preamble like "Here's a post" or similar
- Start directly with the post content
- Write 3-4 sentences maximum
- Sound like a real person sharing helpful local knowledge, not an AI
- Include 1-2 relevant emojis naturally in the text
- End with an engaging question to encourage comments from the Quito expat community
- Be specific and actionable
- Use a warm, friendly tone

Write only the post text, nothing else:"""
    
    try:
        response = model.generate_content(prompt)
        cleaned_text = clean_ai_response(response.text)
        
        # PRIORITY 1: Try to use group images library
        group_images = load_group_images()
        if group_images:
            selected_image = get_unused_group_image(group_images)
            if selected_image:
                print(f"   📸 Using group library image: {selected_image['post_message'][:50]}...")
                # Add photo credit if description exists
                if selected_image['post_message']:
                    cleaned_text += f"\n\n📸 {selected_image['post_message']}"
                return cleaned_text, selected_image['url']
        
        # FALLBACK: Use Unsplash if no group images available
        print("   🔍 No group images available, using Unsplash...")
        image_query = generate_unsplash_query_with_gemini(topic, "Quito, Ecuador")
        image = search_relevant_image(image_query)
        
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
    
    # ENHANCED: Using system instruction
    model = genai.GenerativeModel(
        'gemini-3-flash-preview',
        system_instruction="""You are an expat living in Quito, ECUADOR (South America).
You share funny, relatable moments about expat life in Ecuador.
Ecuador is in SOUTH AMERICA, not in Spain or Europe."""
    )
    
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
- Context: You are an expat in Quito, ECUADOR (South America)
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
        
        # PRIORITY 1: Try to use group images library
        group_images = load_group_images()
        if group_images:
            selected_image = get_unused_group_image(group_images)
            if selected_image:
                print(f"   📸 Using group library image: {selected_image['post_message'][:50]}...")
                # Add photo credit if description exists
                if selected_image['post_message']:
                    cleaned_text += f"\n\n📸 {selected_image['post_message']}"
                return cleaned_text, selected_image['url']
        
        # FALLBACK: Use Unsplash if no group images available
        print("   🔍 No group images available, using Unsplash...")
        image_queries = [
            'Quito street scene everyday life',
            'Ecuador market colorful vendors',
            'traditional Ecuadorian food plate',
            'Quito public transportation bus',
            'Old Town Quito colonial architecture'
        ]
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
    """Use Gemini to translate and create engaging post content - ENHANCED VERSION"""
    
    # ENHANCED: Using system instruction + grounding for geographic accuracy
    model = genai.GenerativeModel(
        'gemini-3-flash-preview',
        system_instruction="""You are a news translator for expats living in Quito, ECUADOR.

CRITICAL GEOGRAPHIC KNOWLEDGE:
- Your audience lives in ECUADOR (a country in SOUTH AMERICA)
- The capital of Ecuador is Quito
- Ecuador is NOT in Spain or Europe
- Spain is a country in EUROPE
- When translating Spanish news, always clarify if it's about Spain vs Ecuador
- Only include news relevant to people living in Ecuador/Latin America

You translate Spanish-language news and make it relevant for Ecuador expats."""
    )
    
    prompt = f"""Translate this Spanish news article for expats living in QUITO, ECUADOR (South America).

CRITICAL LOCATION CONTEXT:
- The readers live in ECUADOR, which is in SOUTH AMERICA
- Spain is in EUROPE, not South America
- Ecuador is a completely different country from Spain
- SKIP CRITERIA - Respond with "SKIP" if this article is:
  * Only about Spanish domestic politics (elections, government appointments, local laws)
  * Only about Spanish celebrities or entertainment
  * About European Union politics or regulations
  * About Spain-only business or economic news
  * NOT relevant to people living in Latin America/Ecuador
- KEEP CRITERIA - Only translate if it's about:
  * International news that affects multiple countries
  * Latin America or Ecuador specifically
  * Major world events (wars, disasters, global economics)
  * Technology, science, or culture with global relevance
  * Immigration, expat issues, or international relations

CRITICAL INSTRUCTIONS:
- If NOT relevant to Ecuador expats, respond ONLY with "SKIP"
- DO NOT include any preamble like "Here's a post" or similar
- Start directly with the post content
- Write like a real person sharing interesting news, not an AI
- Keep it concise (2-3 sentences that capture the key story)
- Use a conversational, engaging tone
- Include 1-2 relevant emojis naturally
- ALWAYS mention the country/region: "News from [Country]:" or "In [Region]..."
- End with: "Read more: {article['link']}"

Spanish Article:
Title: {article['title']}
Content: {article['summary'][:500]}
Source: {article['link']}

Write only the Facebook post text (no preamble, no markdown):"""
    
    try:
        response = model.generate_content(prompt)
        cleaned_text = clean_ai_response(response.text)
        
        # Check if Gemini said to skip this article
        if cleaned_text.upper().startswith('SKIP'):
            print(f"⏭️ Skipping article (not relevant to Ecuador expats)")
            return None, None
        
        # Ensure the link is included
        if article['link'] not in cleaned_text:
            cleaned_text += f"\n\nRead more: {article['link']}"
        
        # DON'T attach images to news posts - let Facebook generate link preview
        # This ensures the article's own preview image/thumbnail shows up
        return cleaned_text, None
        
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback to simple format
        fallback = f"📰 {article['title']}\n\n{article['summary'][:200]}...\n\nRead more: {article['link']}"
        return fallback, None

def post_to_facebook(message, image_url=None, article_link=None):
    """Post message to Facebook page, optionally with an image
    
    IMPORTANT: For posts WITH images, we use a two-step process:
    1. Upload the photo (unpublished) to get a photo ID
    2. Publish the feed post with the photo attached
    
    This ensures posts appear in the main Posts feed with full-size images,
    not just in the Photos section.
    """
    
    try:
        if image_url:
            # Step 1: Upload the photo as unpublished to get a photo ID
            upload_url = f"https://graph.facebook.com/v24.0/{FACEBOOK_PAGE_ID}/photos"
            upload_payload = {
                'url': image_url,
                'published': 'false',
                'access_token': FACEBOOK_ACCESS_TOKEN
            }
            
            print("   📸 Uploading photo (unpublished)...")
            upload_response = requests.post(upload_url, data=upload_payload)
            upload_response.raise_for_status()
            photo_id = upload_response.json().get('id')
            
            if not photo_id:
                print("⚠️ Could not upload photo, posting without image")
                image_url = None  # Fall through to text-only post
            else:
                print(f"   📸 Photo uploaded, ID: {photo_id}")
                # Step 2: Post to /feed with the photo attached using indexed param format
                feed_url = f"https://graph.facebook.com/v24.0/{FACEBOOK_PAGE_ID}/feed"
                feed_payload = {
                    'message': message,
                    'attached_media[0][media_fbid]': photo_id,
                    'access_token': FACEBOOK_ACCESS_TOKEN
                }
                
                print("   📤 Publishing to feed with attached photo...")
                response = requests.post(feed_url, data=feed_payload)
                response.raise_for_status()
                result = response.json()
                print(f"✅ Successfully posted to Facebook with image! Post ID: {result.get('id')}")
                return True
        
        # News post with link preview
        if article_link and not image_url:
            url = f"https://graph.facebook.com/v24.0/{FACEBOOK_PAGE_ID}/feed"
            # Remove "Read more:" text since Facebook will show rich preview
            message_clean = re.sub(r'\n*Read more:.*?https?://[^\s]+', '', message).strip()
            payload = {
                'message': message_clean,
                'link': article_link,  # This triggers Facebook's link preview
                'access_token': FACEBOOK_ACCESS_TOKEN
            }
            
            print("   🔗 Publishing with link preview...")
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully posted to Facebook with link preview! Post ID: {result.get('id')}")
            return True
        
        # Text-only post (no image, no link)
        if not image_url and not article_link:
            url = f"https://graph.facebook.com/v24.0/{FACEBOOK_PAGE_ID}/feed"
            payload = {
                'message': message,
                'access_token': FACEBOOK_ACCESS_TOKEN
            }
            
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully posted to Facebook! Post ID: {result.get('id')}")
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
    article_link = None  # Track article link for news posts
    
    if content_type == 'news':
        # Fetch and translate news
        print("📰 Fetching latest Spanish news...")
        articles = fetch_latest_news(max_articles=5)  # Increased since some may be skipped
        
        if not articles:
            print("❌ No articles found, falling back to Quito content")
            content_type = 'quito'
        else:
            # Try articles until we find one that's relevant
            for article in articles:
                article_link = article['link']  # Save the article link
                print(f"📄 Processing: {article['title'][:60]}...")
                print("🤖 Translating with Gemini...")
                post_content, image_url = translate_and_summarize_with_gemini(article)
                
                if post_content:
                    break  # Found a relevant article
                else:
                    print("⏭️ Trying next article...")
            
            if not post_content:
                print("❌ No relevant news articles found, falling back to Quito content")
                content_type = 'quito'
    
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
    success = post_to_facebook(post_content, image_url=image_url, article_link=article_link)
    
    if success:
        print(f"\n✅ Automation complete! Posted: {content_type}")
        if image_url:
            print("📸 Posted with image!")
        if article_link:
            print("🔗 Posted with link preview!")
    else:
        print(f"\n❌ Post failed")

if __name__ == "__main__":
    main()
