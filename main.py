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
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return " ".join(clean.split()[:12])

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
    headline = news[0]['title'].split(' - ')[0] if news else "AI Innovation 2026"
    print(f"📰 News: {headline}")

    # 3. GENERATE IMAGE WITH RETRY LOGIC (Fixes 502 Error)
    prompt = clean_prompt(headline)
    encoded_prompt = urllib.parse.quote(f"{prompt} futuristic digital art 8k")
    
    # We will try 3 times if we get a 502 error
    for attempt in range(1, 4):
        try:
            # Change the model slightly on retries to hit different sub-servers
            model = "flux" if attempt == 1 else "turbo"
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&model={model}"
            
            print(f"🎨 Attempt {attempt}: Requesting image...")
            response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=45)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.convert('RGB').save('post.jpg', 'JPEG')
                print("✅ Image verified and saved.")
                break # Success! Exit the loop.
            elif response.status_code == 502:
                print(f"⚠️ Server Overloaded (502). Waiting 15s to retry...")
                time.sleep(15)
            else:
                print(f"❌ API Error {response.status_code}. Skipping...")
                return
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            if attempt == 3: return
            time.sleep(10)
    else:
        print("❌ Could not get image after 3 attempts.")
        return

    # 4. POST TO INSTAGRAM
    try:
        time.sleep(5)
        caption = f"🚀 AI UPDATE: {headline}\n\nStay ahead with @neuralbytes2026 🤖\n\n#AI #TechNews #NeuralBytes"
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
