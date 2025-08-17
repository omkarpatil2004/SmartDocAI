import ffmpeg
import os
import tempfile

def extract_audio_from_video(video_path, audio_path="temp_audio.wav"):
    """
    Extracts audio from a video file using ffmpeg-python.
    Saves audio as mono 16kHz WAV for Whisper.
    """
    try:
        # Use ffmpeg to convert video -> audio
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except Exception as e:
        raise RuntimeError(f"FFmpeg extraction failed: {e}")


def transcribe_video(video_path, model=None):
    """
    Extract audio from video and transcribe it using Whisper.
    """
    # Create temp file for audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
        audio_path = tmp_audio.name

    audio_path = extract_audio_from_video(video_path, audio_path)

    if model is None:
        import whisper
        model = whisper.load_model("base")

    result = model.transcribe(audio_path)
    text = result["text"]

    # cleanup temp file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return text
