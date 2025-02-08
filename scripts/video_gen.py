import requests
import time

# ✅ Use the same authentication format that worked for your credits request
D_ID_API_KEY = "Basic YzJGaGRIWnBhM0J5WVdSb1lXNUFaMjFoYVd3dVkyOXQ6eENhNmRmVkp6b2NsUjVJM2RXNjBS"  # Replace with your working API key

IMAGE_URL = "https://adsculptai.us/Unknown.jpg"  # ✅ Ed Sheeran's image
AUDIO_URL = "https://adsculptai.us/ad_audio.mp3"

def generate_ai_video():
    """Creates a talking AI video using Ed Sheeran's AI voice."""
    
    url = "https://api.d-id.com/talks"
    
    headers = {
        "Authorization": D_ID_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "source_url": IMAGE_URL,  # ✅ Ed Sheeran's image
        "script": {
            "type": "audio",  # ✅ Use audio instead of text
            "audio_url": AUDIO_URL  # ✅ Hosted AI voice file
        },
        "config": {
            "stitch": True  # ✅ Ensures full image is retained
        }
    }
    
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        response_json = response.json()
        talk_id = response_json.get("id", "")
        print(f"✅ Video request created! Talk ID: {talk_id}")

        # ✅ Poll API until the video is ready
        video_url = wait_for_video(talk_id)
        if video_url:
            print(f"🎥 AI Video is ready! Download it here: {video_url}")
        else:
            print("❌ Error: Video processing failed.")
    
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")

def wait_for_video(talk_id):
    """Checks the status of the generated AI video and returns the result URL when ready."""
    
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {"Authorization": D_ID_API_KEY}
    
    while True:
        time.sleep(10)  # ✅ Wait 10 seconds before checking again
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get("status", "")
            if status == "done":
                video_url = response_json.get("result_url", "")
                print(f"✅ Video is ready! 🎥 Download here: {video_url}")
                return video_url
            elif status == "failed":
                print("❌ Error: Video processing failed.")
                return None
            else:
                print(f"⏳ Still processing... Status: {status}")
        else:
            print(f"❌ Error checking video status: {response.status_code}")
            return None

generate_ai_video()