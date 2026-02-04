import os
import time
import requests
import urllib.parse
import re
from gnews import GNews
from instagrapi import Client
from PIL import Image

def clean_prompt(text):
    # Sanitize the headline: remove special characters and keep it short
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return " ".join(clean.split()[:12]) # Limit to 12 words for a clean URL

def run_bot():
    cl = Client()
    
    # 1. Load Session
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("✅ Session loaded.")
    else:
        print("❌ Error: session.json missing.")
        return

    # 2. Fetch News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    
    if news:
        # Clean headline (removes source like "- The Motley Fool")
        headline = news[0]['title'].split(' - ')[0]
        print(f"📰 News Found: {headline}")
    else:
        headline = "AI technology is evolving rapidly today"

    # 3. Generate Image with URL Sanitization
    prompt = clean_prompt(headline)
    encoded_prompt = urllib.parse.quote(f"{prompt}, cinematic digital art, 8k")
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    try:
        print(f"🎨 Generating image for: {prompt}")
        response = requests.get(image_url, timeout=30)
        
        # Save the file
        with open("post.jpg", "wb") as f:
            f.write(response.content)
            
        # VERIFICATION: Check if it's actually an image
        with Image.open("post.jpg") as img:
            img.verify()
        print("✅ Image verified as valid JPEG.")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        # If image fails, do not proceed to upload to avoid banning
        return

    # 4. Upload to Instagram
    try:
        # Standardize format and size for Instagram
        caption = f"🚀 AI NEWS: {headline}\n\nStay updated with @neuralbytes2026 🤖\n\n#AI #NeuralBytes #TechNews"
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! Live at: https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
