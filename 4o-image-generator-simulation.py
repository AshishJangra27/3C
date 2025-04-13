from PIL import Image
from tqdm.auto import tqdm
import cv2
import numpy as np

# Load and convert image to RGB
image_path = "img.png"
img = Image.open(image_path).convert("RGB")

# Get image dimensions
width, height = img.size
block_size = 32  # Adjust as needed

# Convert PIL image to NumPy array
img_np = np.array(img)

# Create an empty (black) canvas
canvas_np = np.zeros((height, width, 3), dtype=np.uint8)

# Setup MP4 video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_path = "final_video.mp4"
fps = 30  # Higher FPS = shorter video
video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

# Define block positions (top to bottom, left to right)
block_positions = [
    (top, left)
    for top in range(0, height, block_size)
    for left in range(0, width, block_size)
]

# Optional: only write every n-th frame
frame_interval = 2

# Process and save video
for i, (top, left) in enumerate(tqdm(block_positions, desc="Creating MP4")):
    right = min(left + block_size, width)
    bottom = min(top + block_size, height)

    # Paste block into canvas
    canvas_np[top:bottom, left:right] = img_np[top:bottom, left:right]

    # Convert RGB to BGR and write every n-th frame
    if i % frame_interval == 0 or i == len(block_positions) - 1:
        frame_bgr = cv2.cvtColor(canvas_np, cv2.COLOR_RGB2BGR)
        video_writer.write(frame_bgr)

# Release the video file
video_writer.release()
print("✅ Video saved to:", video_path)
