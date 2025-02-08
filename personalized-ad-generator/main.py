import os
import time
import re
import requests
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# FastAPI App Initialization
app = FastAPI()
# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# API Keys (Replace with your actual keys)
OPENAI_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_85062ac4fae98315e2f161b56ebd053bfc6f81754bda5244"
D_ID_API_KEY = "Basic YzJGaGRIWnBhM0J5WVdSb1lXNUFaMjFoYVd3dVkyOXQ6bXZldTR4VmJQcDhaNk1rUUhzOHVW"

# ✅ Artist-to-Voice Mapping (ElevenLabs)
ARTIST_VOICE_IDS = {
    "Ed Sheeran": "dSwNjPjWiGXSMuNwpPaS",
    "Lebron James": "x40j5GMEHyWviUJ1Z28Z",
    "Tom Brady": "HbcZPzAeinuI00wgYYfA",
    "Sachin Tendulkar": "Nfj9wej5dcm46RDrLMY0",
    "Virat Kohli": "rqPH8NxL8m3M0jBBUIRz",
    "Stephan Curry": "SWw3OcpT2fZABUh6QmoS",
    "Ronaldo": "dSwNjPjWiGXSMuNwpPaS",
    "Tom Holland": "SN3hIZgUdHv3Fl75Yxr0"
}

# ✅ Artist-to-Image Mapping (D-ID)
ARTIST_IMAGES = {
    "Tom Holland": "https://adsculptai.us/tomholland.jpeg",
    "Ed Sheeran": "https://adsculptai.us/edsheeran.jpeg",
    "Lebron James": "https://adsculptai.us/lebronjames.jpeg",
    "Tom Brady": "https://adsculptai.us/tombrady.jpeg",
    "Sachin Tendulkar": "https://adsculptai.us/sachintendulkar.jpeg",
    "Virat Kohli": "https://adsculptai.us/viratkohli.jpeg",
    "Stephan Curry": "https://adsculptai.us/stephcurry.jpeg",
    "Ronaldo": "https://adsculptai.us/ronaldo.jpeg"
}

# ✅ Brand-to-Logo Mapping
BRAND_LOGOS = {
    "Adidas": "https://adsculptai.us/adiddas_Logo.png",
    "AppLoving": "https://adsculptai.us/appLovin_logo.png",
    "Benetton": "https://adsculptai.us/Benetton_logo.webp",
    "Chanel": "https://adsculptai.us/chanel_logo.png",
    "LV": "https://adsculptai.us/LV_logo.png",
    "MRF": "https://adsculptai.us/MRF_logo.png",
    "Oracle": "https://adsculptai.us/Oracle_Logo.png",
    "Redbull": "https://adsculptai.us/redbull_logo.webp"
}


AUDIO_FILES_IDS = {
    "Ed Sheeran": "https://adsculptai.us/ad_audio_edsheeran.mp3",
    "Lebron James": "https://adsculptai.us/ad_audio_lebronjames.mp3",
    "Tom Brady": "https://adsculptai.us/ad_audio_tombrady.mp3",
    "Sachin Tendulkar": "https://adsculptai.us/ad_audio_sachintendulkar.mp3",
    "Virat Kohli": "https://adsculptai.us/ad_audio_viratkohli.mp3",
    "Stephan Curry": "https://adsculptai.us/ad_audio_stephcurry.mp3",
    "Ronaldo": "https://adsculptai.us/ad_audio_ronaldo.mp3",
    "Tom Holland": "https://adsculptai.us/ad_audio_tomholland.mp3"
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
    script_file = "ad_script.txt"

    if not os.path.exists(script_file):
        print(f"❌ Error: {script_file} not found.")
        return ""

    with open(script_file, "r") as file:
        script_content = file.readlines()

    dialogue_lines = []

    for line in script_content:
        cleaned_line = line.strip()
        
        # Remove scene directions (anything inside **[ ]**)
        cleaned_line = re.sub(r"\*\*.*?\*\*", "", cleaned_line).strip()

        if cleaned_line:
            dialogue_lines.append(cleaned_line)

    extracted_dialogue = "\n".join(dialogue_lines)

    if not extracted_dialogue:
        print("❌ Error: No dialogue extracted.")
    
    return extracted_dialogue

# === Step 3: Generate AI Voice ===
def generate_voice(voice_id):
    """Generates AI voice from the script using ElevenLabs."""
    dialogue = extract_dialogue()

    if not dialogue:
        print("❌ Error: No text found for voice generation.")
        return

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

    if response.status_code == 200:
        with open("ad_audio.mp3", "wb") as f:
            f.write(response.content)
        print("✅ AI voice saved as 'ad_audio.mp3'.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# === Step 4: Generate AI Video ===
def generate_ai_video(image_url, artist):
    """Creates AI-generated video with D-ID API using artist-specific audio file."""

    # ✅ Get the correct audio file URL for the artist
    AUDIO_URL = AUDIO_FILES_IDS.get(artist, None)

    if not AUDIO_URL:
        print(f"❌ Error: No audio file found for artist '{artist}'")
        return None

    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": D_ID_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "source_url": image_url,
        "script": {
            "type": "audio",
            "audio_url": AUDIO_URL  # ✅ Now uses artist-specific audio file
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
            if response_json.get("status") == "done":
                return response_json.get("result_url", "")
        print("⏳ Still processing...")

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

    # 2️⃣ Generate AI Video with Artist-Specific Audio
    video_url = generate_ai_video(ARTIST_IMAGES[artist], artist)  # ✅ Fix applied

    if video_url:
        return {"video_url": video_url}
    else:
        raise HTTPException(status_code=500, detail="Video generation failed.")

# === Run FastAPI Server ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)