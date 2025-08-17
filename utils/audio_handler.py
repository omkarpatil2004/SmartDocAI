import whisper

def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # options: tiny, base, small, medium, large
    result = model.transcribe(audio_path)
    return result["text"]
