import os
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client

def run_bot():
    # 1. Get News
    gn = GNews(language='en', period='1d', max_results=1)
    news = gn.get_news('Artificial Intelligence')
    headline = news[0]['title'] if news else "AI is changing the world."
    
    # 2. Make Image
    prompt = urllib.parse.quote(f"{headline}, futuristic digital art, 8k, cinematic")
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true"
    with open("post.jpg", "wb") as f:
        f.write(requests.get(url).content)
        
    # 3. Post
    cl = Client()
    cl.login(os.environ["INSTA_USER"], os.environ["INSTA_PASS"])
    cl.photo_upload("post.jpg", f"{headline}\n\n#AI #neuralbytes2026")

if __name__ == "__main__":
    run_bot()
