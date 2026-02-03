from __future__ import annotations
import os
import time
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client

def run_bot():
    cl = Client()
    # 1. Add a small delay before starting
    time.sleep(5) 
    
    print("Attempting login...")
    cl.login(os.environ["INSTA_USER"], os.environ["INSTA_PASS"])
    
    # 2. Get News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    headline = news[0]['title'] if news else "The future of technology is here."
    
    # 3. Create Visual
    prompt = urllib.parse.quote(f"{headline}, hyper-realistic, futuristic digital art, 8k")
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true"
    
    with open("post.jpg", "wb") as f:
        f.write(requests.get(url).content)
        
    # 4. Post with a delay
    print("Uploading...")
    time.sleep(10)
    cl.photo_upload("post.jpg", f"🚀 TECH NEWS: {headline}\n\n#AI #neuralbytes2026")
    print("Done!")

if __name__ == "__main__":
    run_bot()
