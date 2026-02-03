import os
import requests
import urllib.parse
from gnews import GNews
from instagrapi import Client

def run_automation():
    # 1. GET THE LATEST TECH NEWS
    google_news = GNews(language='en', period='1d', max_results=1)
    news = google_news.get_news('Technology')
    headline = news[0]['title'] if news else "The Future of AI is here."

    # 2. CREATE A HIGH-END VISUAL
    # We add "artistic" words to make the AI output look premium
    art_prompt = f"{headline}, cinematic lighting, futuristic 8k digital art, unreal engine 5"
    encoded_prompt = urllib.parse.quote(art_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&nologo=true"
    
    img_data = requests.get(image_url).content
    with open("post.jpg", "wb") as f:
        f.write(img_data)

    # 3. UPLOAD TO NEURALBYTES2026
    cl = Client()
    cl.login(os.environ["INSTA_USER"], os.environ["INSTA_PASS"])
    cl.photo_upload("post.jpg", f"🚀 TECH NEWS: {headline}\n\n#AI #Tech #neuralbytes2026")

if __name__ == "__main__":
    run_automation()
