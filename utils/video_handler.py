from moviepy.editor import VideoFileClip
from utils.audio_handler import transcribe_audio

def transcribe_video(video_path):
    clip = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path)
    return transcribe_audio(audio_path)
