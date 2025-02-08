import requests
import re

ELEVENLABS_API_KEY = "sk_18861a274597c819a0d7f305018618dce3b1df1e49c1ac30"
VOICE_ID = "dSwNjPjWiGXSMuNwpPaS"

def extract_dialogue(script_file):
    """Extract only spoken lines from the script, ignoring scene directions."""
    with open(script_file, "r") as file:
        script_content = file.read()

    # Use regex to remove scene directions (anything between **[ ]**)
    script_content = re.sub(r"\*\*.*?\*\*", "", script_content)

    return script_content.strip()

def generate_voice():
    """Generate AI voice only for spoken lines."""
    dialogue = extract_dialogue("ad_script.txt")  # Get cleaned script

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": dialogue,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
    }
    
    response = requests.post(url, json=data, headers=headers)

    # Save the AI-generated voice
    with open("ad_audio.mp3", "wb") as f:
        f.write(response.content)
    
    print("✅ AI voice saved as 'ad_audio.mp3'")

generate_voice()
