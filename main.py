import cv2
import numpy as np
import time
import random
from moviepy.editor import VideoFileClip, AudioFileClip

# Function to draw a heart shape
def draw_heart(frame, x, y, size=10, color=(0, 0, 255)):
    pts = np.array([
        [x, y],
        [x - size, y - size],
        [x - int(size * 1.5), y - size * 2],
        [x, y - size * 3],
        [x + int(size * 1.5), y - size * 2],
        [x + size, y - size]
    ], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(frame, [pts], color)

# Function to draw message text
def draw_message(frame, message, position, font_scale=1, color=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, message, position, font, font_scale, color, 2, cv2.LINE_AA)

# Initialize camera
cap = cv2.VideoCapture(0)

# Output video settings
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('birthday_gift_for_mom.mp4', fourcc, 20.0, (640, 480))

# Heart animation list
hearts = []

start_time = time.time()
duration = 20  # video length in seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    current_time = time.time()

    # Add new hearts randomly
    if random.randint(0, 10) > 7:
        hearts.append([random.randint(50, 590), 480])

    # Animate existing hearts
    new_hearts = []
    for h in hearts:
        draw_heart(frame, h[0], h[1], size=10)
        h[1] -= 5  # move up
        if h[1] > 0:
            new_hearts.append(h)
    hearts = new_hearts

    # Add birthday messages
    draw_message(frame, "Happy Birthday Maaa!", (80, 50), font_scale=1.5, color=(255, 0, 255))
    draw_message(frame, "You're the best!", (180, 440), font_scale=1, color=(143, 0, 255))

    # Show the video frame
    cv2.imshow('Birthday Magic Mirror', frame)

    # Write the frame to output file
    out.write(frame)

    # Exit conditions
    if current_time - start_time > duration or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()


from moviepy.editor import VideoFileClip, AudioFileClip

# Load your silent video
video = VideoFileClip("birthday_gift_for_mom.mp4")

# Load the audio file
audio_full = AudioFileClip("song.mp3")

# Calculate the minimum duration between video and audio
min_duration = min(video.duration, audio_full.duration)

# Use that minimum duration for subclip
audio = audio_full.subclip(0, min_duration)

# Set the audio to the video (also subclip the video if needed)
final_video = video.subclip(0, min_duration).set_audio(audio)

# Export the final video
final_video.write_videofile("birthday_with_music.mp4", codec="libx264", audio_codec="aac")
