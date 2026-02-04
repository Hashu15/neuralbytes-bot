import os
import time
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client
from PIL import Image  # This verifies if the image is real

def run_bot():
    cl = Client()
    
    # 1. LOAD SESSION (The Golden Key)
    if os.path.exists("session.json"):
        try:
            cl.load_settings("session.json")
            print("✅ Session loaded.")
        except Exception as e:
            print(f"❌ Could not load session file: {e}")
            return
    else:
        print("❌ Error: session.json not found! Upload it to GitHub first.")
        return

    # 2. GET LATEST AI NEWS
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    
    if news:
        headline = news[0]['title']
        print(f"📰 News Found: {headline}")
    else:
        headline = "AI is transforming the digital landscape today."
        print("⚠️ No news found, using default headline.")

    # 3. GENERATE & VERIFY IMAGE
    # We use a 1:1 square ratio (1024x1024) which Instagram loves
    prompt = urllib.parse.quote(f"{headline}, futuristic digital art, cinematic lighting, 8k, detailed")
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1024&height=1024&nologo=true"
    
    try:
        img_data = requests.get(image_url, timeout=30).content
        with open("post.jpg", "wb") as handler:
            handler.write(img_data)
        
        # SAFETY CHECK: Use PIL to see if this is actually an image
        with Image.open("post.jpg") as img:
            img.verify()
        print("✅ Image verified as valid JPEG.")
    except Exception as e:
        print(f"❌ Image Error: The file downloaded is not a valid image. Error: {e}")
        return

    # 4. POST TO INSTAGRAM (Safe Mode)
    try:
        # Add a small human-like delay
        time.sleep(10)
        
        caption = (
            f"🚀 AI UPDATE: {headline}\n\n"
            f"Follow @neuralbytes2026 for daily AI insights! 🤖\n\n"
            f"#AI #TechNews #NeuralBytes #ArtificialIntelligence #MachineLearning"
        )
        
        # The actual upload
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! Post is live: https://www.instagram.com/p/{media.code}/")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
