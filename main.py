import os
import time
import requests
import urllib.parse
import re
from gnews import GNews
from instagrapi import Client
from PIL import Image

def clean_prompt(text):
    # Remove special characters like quotes, dashes, and parentheses
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Limit to the first 15 words to keep the URL short and safe
    return " ".join(clean.split()[:15])

def run_bot():
    cl = Client()
    
    # 1. LOAD SESSION
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("✅ Session loaded.")
    else:
        print("❌ session.json missing.")
        return

    # 2. GET NEWS
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    
    if news:
        raw_headline = news[0]['title']
        # Remove the source (e.g., "- The Motley Fool") from the headline
        headline = raw_headline.split(' - ')[0]
        print(f"📰 News Found: {headline}")
    else:
        headline = "AI technology is advancing rapidly today"
        print("⚠️ Default headline used.")

    # 3. GENERATE IMAGE (The Fixed Part)
    # We clean the headline to make it a safe prompt
    safe_prompt = clean_prompt(headline)
    encoded_prompt = urllib.parse.quote(f"{safe_prompt}, futuristic digital art, 8k")
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    
    try:
        print(f"🎨 Requesting image for: {safe_prompt}")
        response = requests.get(image_url, timeout=30)
        with open("post.jpg", "wb") as f:
            f.write(response.content)
        
        # Verify the image is real
        with Image.open("post.jpg") as img:
            img.verify()
        print("✅ Image verified.")
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    # 4. POST TO INSTAGRAM
    try:
        time.sleep(5)
        caption = f"🚀 AI NEWS: {headline}\n\nFollow @neuralbytes2026 for more! 🤖\n\n#AI #Tech #NeuralBytes"
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! Live at: https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
