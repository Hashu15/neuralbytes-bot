import os
import time
import random
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client
from PIL import Image
from io import BytesIO

def run_bot():
    cl = Client()
    
    # 1. SETUP STEALTH MODE
    # Randomize the 'Device ID' each time to look like a new login attempt
    cl.set_device({
        "app_version": "269.0.0.18.75",
        "android_version": "26",
        "android_release": "8.0.0",
        "model": "SM-G960F",
        "manufacturer": "samsung"
    })

    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("✅ Session loaded.")
    else:
        print("❌ session.json missing.")
        return

    # 2. GET NEWS & IMAGE (Same as before)
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    headline = news[0]['title'].split(' - ')[0] if news else "AI Innovation"
    
    # Try AI image, fallback to Unsplash
    img_data = None
    try:
        encoded = urllib.parse.quote(headline[:50])
        res = requests.get(f"https://image.pollinations.ai/prompt/{encoded}?nologo=true", timeout=15)
        if res.status_code == 200: img_data = res.content
    except: pass
    
    if not img_data:
        res = requests.get("https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1080", timeout=15)
        img_data = res.content

    with Image.open(BytesIO(img_data)).convert('RGB') as img:
        img.save('post.jpg', 'JPEG')

    # 3. POST WITH RETRY LOGIC (The Fix)
    caption = f"🚀 AI UPDATE: {headline}\n\nStay ahead with @neuralbytes2026 🤖\n\n#AI #TechNews #NeuralBytes"
    
    for attempt in range(1, 4):
        try:
            # Add a long, random delay (30-60 seconds) to act human
            wait_time = random.randint(30, 60)
            print(f"🕒 Attempt {attempt}: Waiting {wait_time}s to avoid bot detection...")
            time.sleep(wait_time)
            
            media = cl.photo_upload("post.jpg", caption)
            print(f"🎉 SUCCESS! https://www.instagram.com/p/{media.code}/")
            break 
        except Exception as e:
            if "AuthorizationFailedError" in str(e) and attempt < 3:
                print(f"⚠️ Temporary failure. Retrying attempt {attempt+1}...")
                continue
            else:
                print(f"❌ Final Upload failed: {e}")
                break

if __name__ == "__main__":
    run_bot()
