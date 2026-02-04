import os
import time
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client
from PIL import Image
from io import BytesIO

def get_ai_image(prompt):
    """Try to generate an AI image from Pollinations."""
    encoded = urllib.parse.quote(f"{prompt} futuristic digital art 8k")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"
    try:
        print("🎨 Attempting AI Generation...")
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

def get_fallback_image(query):
    """Fallback: Get a high-quality tech photo from Unsplash (No API key needed for basic source)."""
    print("🛰️ AI Down. Switching to Unsplash Fallback...")
    # This uses Unsplash Source to find a high-quality photo based on your news keywords
    query_encoded = urllib.parse.quote(query)
    url = f"https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1080&q=80" # Default High-Tech Robot
    
    # Try to get a more specific tech image
    tech_url = f"https://source.unsplash.com/1080x1080/?technology,ai,{query_encoded}"
    try:
        res = requests.get(tech_url, timeout=15)
        if res.status_code == 200:
            return res.content
    except:
        pass
    return requests.get(url).content # Return the reliable robot photo if search fails

def run_bot():
    cl = Client()
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("✅ Session loaded.")
    else: return

    # 1. Get News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    headline = news[0]['title'].split(' - ')[0] if news else "The Future of AI"
    print(f"📰 News: {headline}")

    # 2. Get Image (AI first, then Unsplash)
    img_data = get_ai_image(headline[:50])
    if not img_data:
        img_data = get_fallback_image("artificial intelligence")

    # 3. Verify & Save
    try:
        img = Image.open(BytesIO(img_data))
        img.convert('RGB').save('post.jpg', 'JPEG')
        print("✅ Image Ready.")
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    # 4. Post
    try:
        caption = f"🚀 AI UPDATE: {headline}\n\nStay ahead with @neuralbytes2026 🤖\n\n#AI #TechNews #NeuralBytes"
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
