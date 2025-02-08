import os
import time
import re
import requests
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI App Initialization
app = FastAPI()

# ✅ API Keys (Replace with your actual keys)
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ELEVENLABS_API_KEY = "sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
D_ID_API_KEY = "Basic xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ✅ Artist-to-Voice Mapping (ElevenLabs)
ARTIST_VOICE_IDS = {
    "Ed Sheeran": "dSwNjPjWiGXSMuNwpPaS",
    "Taylor Swift": "aBcdEfGhIjKlMnOpQrSt",
    "Drake": "xYz1234567890AbCdEfGh",
}

# ✅ Artist-to-Image Mapping (D-ID)
ARTIST_IMAGES = {
    "Ed Sheeran": "https://adsculptai.us/ed_sheeran.jpg",
    "Taylor Swift": "https://adsculptai.us/taylor_swift.jpg",
    "Drake": "https://adsculptai.us/drake.jpg",
}

# ✅ Brand-to-Logo Mapping
BRAND_LOGOS = {
    "Nike": "https://adsculptai.us/nike_logo.png",
    "Adidas": "https://adsculptai.us/adidas_logo.png",
    "Apple": "https://adsculptai.us/apple_logo.png",
}


# === API Request Model ===
class AdRequest(BaseModel):
    artist: str
    product: str
    brand: str


# === Step 1: Generate Ad Script ===
def generate_ad_script(influencer, product):
    """Generates a 30-second ad script using OpenAI."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"Generate a 30-second advertisement script where {influencer} promotes {product}. The tone should be casual, friendly, and engaging."
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    
    script_content = response.choices[0].message.content.strip()

    # Save script
    with open("ad_script.txt", "w") as file:
        file.write(script_content)

    print("✅ Ad script saved.")
    return script_content


# === Step 2: Extract Dialogue (For Voiceover) ===
def extract_dialogue():
    """Extracts spoken lines, removing scene directions."""
    with open("ad_script.txt", "r") as file:
        script_content = file.read()
    
    cleaned_script = re.sub(r"\*\*.*?\*\*", "", script_content).strip()
    return cleaned_script


# === Step 3: Generate AI Voice ===
def generate_voice(voice_id):
    """Generates AI voice from the script using ElevenLabs."""
    dialogue = extract_dialogue()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": dialogue,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
    }
    
    response = requests.post(url, json=data, headers=headers)

    # Save audio file
    with open("ad_audio.mp3", "wb") as f:
        f.write(response.content)

    print("✅ AI voice saved as 'ad_audio.mp3'.")


# === Step 4: Generate AI Video ===
def generate_ai_video(image_url):
    """Creates AI-generated video with D-ID API."""
    AUDIO_URL = "https://adsculptai.us/ad_audio.mp3"  # Hosted audio file

    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": D_ID_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "source_url": image_url,
        "script": {
            "type": "audio",
            "audio_url": AUDIO_URL
        },
        "config": {"stitch": True}
    }
    
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        talk_id = response.json().get("id", "")
        print(f"✅ Video request created! Talk ID: {talk_id}")
        return wait_for_video(talk_id)
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")
        return None


# === Step 5: Poll Until Video is Ready ===
def wait_for_video(talk_id):
    """Checks the video processing status and retrieves the final video URL."""
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {"Authorization": D_ID_API_KEY}

    while True:
        time.sleep(10)
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get("status", "")
            
            if status == "done":
                video_url = response_json.get("result_url", "")
                print(f"🎥 AI Video is ready! Download here: {video_url}")
                return video_url
            elif status == "failed":
                print("❌ Error: Video processing failed.")
                return None
            else:
                print(f"⏳ Still processing... Status: {status}")
        else:
            print(f"❌ Error checking video status: {response.status_code}")
            return None


# === FastAPI Endpoint to Trigger Pipeline ===
@app.post("/generate_ad")
async def generate_ad(request: AdRequest):
    artist = request.artist
    product = request.product
    brand = request.brand

    # ✅ Validate Inputs
    if artist not in ARTIST_VOICE_IDS or artist not in ARTIST_IMAGES:
        raise HTTPException(status_code=400, detail="Artist not found in database.")
    if brand not in BRAND_LOGOS:
        raise HTTPException(status_code=400, detail="Brand not found in database.")

    print(f"🚀 Generating ad for {product} with {artist} for {brand}...")

    # 1️⃣ Generate Ad Script
    generate_ad_script(artist, product)

    # 2️⃣ Generate AI Voice
    generate_voice(ARTIST_VOICE_IDS[artist])

    # 3️⃣ Generate AI Video
    video_url = generate_ai_video(ARTIST_IMAGES[artist])

    if video_url:
        return {"video_url": video_url}
    else:
        raise HTTPException(status_code=500, detail="Video generation failed.")


# === Run FastAPI Server ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
