import os
import time
import requests
import urllib.parse
import re
from gnews import GNews
from instagrapi import Client
from PIL import Image
from io import BytesIO

def clean_prompt(text):
    # Remove all non-alphanumeric characters for a stable URL
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Pollinations works best with prompts under 75 characters
    return " ".join(clean.split()[:10])

def run_bot():
    cl = Client()
    
    # 1. Load Session
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("✅ Session loaded.")
    else:
        print("❌ session.json missing.")
        return

    # 2. Get News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    headline = news[0]['title'].split(' - ')[0] if news else "AI Innovation Today"
    print(f"📰 News: {headline}")

    # 3. Robust Image Generation
    prompt = clean_prompt(headline)
    # Using 'flux' model for higher reliability
    encoded_prompt = urllib.parse.quote(f"{prompt} futuristic digital art 8k")
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&model=flux"
    
    try:
        print(f"🎨 Requesting: {image_url}")
        # Add a real browser header to prevent being blocked as a bot
        response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return

        # Use BytesIO to verify the image in memory before saving
        img = Image.open(BytesIO(response.content))
        img.convert('RGB').save('post.jpg', 'JPEG')
        print("✅ Image verified and saved.")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    # 4. Post with Fail-Safe
    try:
        # Avoid 'checkpoint' by waiting 5 seconds
        time.sleep(5)
        caption = f"🚀 AI UPDATE: {headline}\n\nStay ahead with @neuralbytes2026 🤖\n\n#AI #TechNews #NeuralBytes"
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
