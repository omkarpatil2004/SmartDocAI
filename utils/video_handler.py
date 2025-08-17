import os
import subprocess
from faster_whisper import WhisperModel

def extract_audio_from_video(video_path, audio_path="temp_audio.mp3"):
    """
    Extracts audio from video using ffmpeg
    """
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # no video
        "-acodec", "mp3",
        audio_path,
        "-y"  # overwrite if exists
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return audio_path

def transcribe_video(video_path):
    """
    Extract audio from video and transcribe it using faster-whisper
    """
    audio_path = extract_audio_from_video(video_path)

    # Load Whisper model
    model = WhisperModel("base", device="cpu", compute_type="int8")

    segments, _ = model.transcribe(audio_path)
    transcription = " ".join([segment.text for segment in segments])

    # cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return transcription.strip()
