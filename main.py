import os
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client

def run_bot():
    cl = Client()
    
    # 1. Load the session (The Golden Key)
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("Session loaded successfully!")
    else:
        print("Error: session.json not found.")
        return

    # 2. Get Today's AI News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    
    if news:
        headline = news[0]['title']
        link = news[0]['url']
    else:
        headline = "AI is evolving faster than ever!"
        link = ""

    # 3. Generate the Image
    prompt = urllib.parse.quote(f"{headline}, futuristic digital art, cinematic, 8k")
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true"
    
    with open("post.jpg", "wb") as f:
        f.write(requests.get(image_url).content)

    # 4. Post to Instagram
    try:
        caption = f"🚀 AI UPDATE: {headline}\n\nStay ahead with @neuralbytes2026 🤖\n\n#AI #TechNews #NeuralBytes #ArtificialIntelligence"
        cl.photo_upload("post.jpg", caption)
        print("✅ Post uploaded successfully!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    run_bot()
