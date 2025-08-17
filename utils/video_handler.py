import ffmpeg
import os

def extract_audio_from_video(video_path, audio_path="temp_audio.wav"):
    """
    Extracts audio from a video file using ffmpeg-python (no subprocess).
    Outputs audio in WAV format, mono, 16kHz (good for Whisper/STT).
    """
    try:
        (
            ffmpeg
            .input(video_path)                                  # input video
            .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()                                 # overwrite if exists
            .run(quiet=True)                                    # run silently
        )
        return audio_path
    except Exception as e:
        raise RuntimeError(f"FFmpeg extraction failed: {e}")


def transcribe_video(video_path, model=None):
    """
    Extract audio from video and transcribe it using Whisper or any STT model.
    """
    audio_path = extract_audio_from_video(video_path)

    if model is None:
        import whisper
        model = whisper.load_model("base")   # load small Whisper model by default

    result = model.transcribe(audio_path)
    text = result["text"]

    # cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return text
