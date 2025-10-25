import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using AssemblyAI SDK.
    Returns the transcribed text.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(file_path)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.text
