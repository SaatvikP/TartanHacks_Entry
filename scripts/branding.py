import os
from PIL import Image, ImageDraw, ImageFont

import os
from PIL import Image, ImageDraw, ImageFont

# ✅ Function to Create High-Quality Bold Slides
def create_slide(text, filename):
    """Creates an image slide with centered, bold text."""
    img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))  # Black background
    draw = ImageDraw.Draw(img)

    # ✅ Load a bold font
    try:
        font = ImageFont.truetype("Arial Bold.ttf", 100)  # Use a bold font
    except IOError:
        font = ImageFont.load_default()  # Use default if missing

    # ✅ Calculate text size using `textbbox()` instead of `textsize()`
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    text_position = ((1920 - text_width) // 2, (1080 - text_height) // 2)  # Center text

    draw.text(text_position, text, fill=(255, 255, 255), font=font)

    img.save(filename)
    print(f"✅ Stylish Slide Created: {filename}")

# ✅ Generate Improved Slides
create_slide("🔥 Nike Air Force 1 🔥\nTimeless Classic - $120", "product_slide.png")
create_slide("💥 Available Now! 💥\nwww.nike.com & Select Retailers", "purchase_slide.png")


# ✅ Convert Slides to 3-Second Videos with Bold Text
os.system("ffmpeg -loop 1 -t 3 -i product_slide.png -vf \"scale=1920:1080,format=yuv420p\" -c:v libx264 product_slide.mp4")
os.system("ffmpeg -loop 1 -t 3 -i purchase_slide.png -vf \"scale=1920:1080,format=yuv420p\" -c:v libx264 purchase_slide.mp4")

# ✅ Resize AI Video to Match (Fixes "Input link parameters do not match" error)
os.system("ffmpeg -i ai_video.mp4 -vf \"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black\" -c:v libx264 -crf 23 -preset slow -c:a copy ai_video_resized.mp4")

# ✅ Merge AI Video, Smaller Nike Logo (Bottom Right), and Final Slides
ffmpeg_command = """
ffmpeg -i ai_video_resized.mp4 -i nike_logo.png -i product_slide.mp4 -i purchase_slide.mp4 \
-filter_complex "[0:v][1:v] scale=150:-1,overlay=W-w-40:H-h-40 [v0]; \
[v0] [2:v] [3:v] concat=n=3:v=1:a=0 [v]" \
-map "[v]" -map 0:a -c:v libx264 -c:a copy final_ad.mp4
"""

os.system(ffmpeg_command)

print("✅ Final Nike ad created: final_ad.mp4 (Smaller Logo & Stylish Slides)")
