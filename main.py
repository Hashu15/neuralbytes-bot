import os
import time
import random
import requests
from instagrapi import Client
from PIL import Image
from io import BytesIO

def run_bot():
    cl = Client()
    
    # 1. LOAD SESSION & SYNC DEVICE
    if os.path.exists("session.json"):
        # We load the settings but DO NOT set a new device yet
        cl.load_settings("session.json")
        
        # We force the script to use the device info FROM the session file
        # This prevents the 412 'Mismatch' error
        session_settings = cl.get_settings()
        if "device_settings" in session_settings:
            cl.set_device(session_settings["device_settings"])
            print("✅ Device synced from session.")
        
        print("✅ Session loaded.")
    else:
        print("❌ session.json missing.")
        return

    # 2. DOWNLOAD FALLBACK IMAGE (Since AI is currently 502)
    print("🛰️ Using fallback image...")
    res = requests.get("https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1080", timeout=15)
    with Image.open(BytesIO(res.content)).convert('RGB') as img:
        img.save('post.jpg', 'JPEG')

    # 3. POST WITH DELAY
    caption = "🚀 AI Update: NeuralBytes is testing its automated systems. #AI #NeuralBytes"
    
    try:
        # 412 errors are sensitive to timing. A 30s wait often 'clears' the precondition.
        print("🕒 Waiting 30s to satisfy Instagram security...")
        time.sleep(30)
        
        # We use a lower-level upload method that is more stable
        media = cl.photo_upload("post.jpg", caption)
        print(f"🎉 SUCCESS! https://www.instagram.com/p/{media.code}/")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        if "412" in str(e):
            print("💡 TIP: Your session.json is likely 'stale'.")
            print("Please run get_session.py on your laptop and re-upload the file.")

if __name__ == "__main__":
    run_bot()
