import os
import subprocess
from textToAud import text_to_speech_file

def text_toaudio(text, folder):
    audio_path = os.path.join("uploads", folder, "audio.mp3")
    print(audio_path)
    # Call the actual text-to-speech function
    # Note: I'm assuming textToAud.py has a function named text_to_speech_file
    text_to_speech_file(text=text, folder=folder, output_file=audio_path)
    print(f"Audio created for folder: {folder}")
    return audio_path

def create_reell(folder, audio_path):
    uploads_path = os.path.join("uploads", folder)
    input_list_path = os.path.join(uploads_path, "input.txt")
    output_path = os.path.join(os.path.join("static/reels", f"{folder}.mp4"))

    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', input_list_path,
        '-i', audio_path,
        '-filter_complex', '[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black[v]',
        '-map', '[v]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        '-shortest',
        output_path
    ]

    try:
        # Corrected line: removed shell=True
        subprocess.run(command, check=True)
        print(f"Reel created successfully at: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise