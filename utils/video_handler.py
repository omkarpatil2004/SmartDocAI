import ffmpeg
import os
import tempfile
import shutil

def extract_audio_from_video(video_path, audio_path=None):
    """
    Extracts audio from a video file using ffmpeg-python.
    Ensures proper handling on Streamlit Cloud.
    """
    if audio_path is None:
        tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio_path = tmp_audio.name
        tmp_audio.close()

    try:
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


def transcribe_video(video_file, model=None):
    """
    Takes a Streamlit uploaded file object or file path,
    saves it to a temp file, extracts audio, and transcribes.
    """
    # 1️⃣ Save uploaded video file to temp path
    if hasattr(video_file, "read"):  # file-like object from st.file_uploader
        tmp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        shutil.copyfileobj(video_file, tmp_video)
        tmp_video_path = tmp_video.name
        tmp_video.close()
    else:
        tmp_video_path = video_file  # already a path

    # 2️⃣ Extract audio
    audio_path = extract_audio_from_video(tmp_video_path)

    # 3️⃣ Load Whisper and transcribe
    if model is None:
        import whisper
        model = whisper.load_model("base")

    result = model.transcribe(audio_path)
    text = result["text"]

    # 4️⃣ Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(tmp_video_path):
        os.remove(tmp_video_path)

    return text
