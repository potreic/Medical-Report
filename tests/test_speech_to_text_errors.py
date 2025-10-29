import pytest
from core.speech_to_text import transcribe_audio

def test_transcribe_audio_raises_if_missing_file():
    with pytest.raises(FileNotFoundError):
        transcribe_audio("this/file/does/not/exist.wav")
