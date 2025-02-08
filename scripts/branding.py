import os
import pillow as PIL
from PIL import Image, ImageDraw, ImageFont

def create_slide(text_lines, filename, font_size=180):
    """Creates an image slide with centered, bold text and better formatting."""
    img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))  # Black background
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Arial Bold.ttf", font_size)
    except IOError:
        try:
            # Try alternative fonts if Arial Bold is not available
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Calculate total height of all text lines
    total_height = 0
    line_heights = []
    
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 20  # Add 20px spacing between lines

    # Start y position to center all text vertically
    current_y = (1080 - total_height) // 2

    # Draw each line centered horizontally
    for i, line in enumerate(text_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (1920 - text_width) // 2
        draw.text((x_position, current_y), line, fill=(255, 255, 255), font=font)
        current_y += line_heights[i] + 20

    img.save(filename)
    print(f"Enhanced Slide Created: {filename}")

# Create slides with better formatting
create_slide(
    ["Nike Air Force 1", "Timeless Classic", "$120"],
    "product_slide.png"
)
create_slide(
    ["Available Now!", "www.nike.com", "& Select Retailers"],
    "purchase_slide.png"
)

# Create fade in/out effect for slides using FFmpeg
def create_animated_slide(input_png, output_mp4, duration=3):
    """Creates a video with fade in/out effects from a static image."""
    ffmpeg_command = f"""
    ffmpeg -y -loop 1 -t {duration} -i {input_png} 
    -vf "fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5,scale=1920:1080,format=yuv420p" 
    -c:v libx264 -pix_fmt yuv420p {output_mp4}
    """
    os.system(ffmpeg_command.replace('\n', ' '))

# Create animated slides
create_animated_slide("product_slide.png", "product_slide.mp4")
create_animated_slide("purchase_slide.png", "purchase_slide.mp4")

# Resize AI Video to Match
os.system("""
ffmpeg -y -i ai_video.mp4 
-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" 
-c:v libx264 -crf 23 -preset slow -c:a copy ai_video_resized.mp4
""".replace('\n', ' '))

# Merge everything together
ffmpeg_command = """
ffmpeg -y -i ai_video_resized.mp4 -i product_slide.mp4 -i purchase_slide.mp4 
-filter_complex "[0:v][1:v][2:v] concat=n=3:v=1:a=0 [v]" 
-map "[v]" -map 0:a -c:v libx264 -c:a copy final_ad.mp4
"""
os.system(ffmpeg_command.replace('\n', ' '))

print("Final ad created with enhanced animated slides!")