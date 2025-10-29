import os
import tempfile
import shutil
import importlib
import builtins
import pytest

@pytest.fixture
def temp_dirs(monkeypatch):
    base = tempfile.mkdtemp(prefix="medbot-tests-")
    audio = os.path.join(base, "audio"); os.makedirs(audio, exist_ok=True)
    reports = os.path.join(base, "reports"); os.makedirs(reports, exist_ok=True)
    transcripts = os.path.join(base, "transcripts"); os.makedirs(transcripts, exist_ok=True)

    monkeypatch.setenv("TEMP_DIR", audio)
    monkeypatch.setenv("REPORT_DIR", reports)
    # dummy api keys to satisfy imports
    monkeypatch.setenv("ASSEMBLYAI_API_KEY", "test-aai")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter")

    # reload settings after env set
    from config import settings
    importlib.reload(settings)
    yield {"base": base, "audio": audio, "reports": reports, "transcripts": transcripts}

    shutil.rmtree(base, ignore_errors=True)

@pytest.fixture
def fake_llm(monkeypatch):
    """
    Gantikan ChatOpenAI dengan fake class yang memiliki .invoke() -> object dgn .content
    """
    class _Msg:
        def __init__(self, content): self.content = content

    class FakeChatOpenAI:
        def __init__(self, *args, **kwargs): pass
        def invoke(self, messages):
            # kembalikan output tidak berformat markdown, campur token aneh utk menguji pembersihan
            text = """
Symptoms
- Cough
- Fever

Diagnosis
- Upper respiratory infection

Prescription / Treatment Plan
- Paracetamol 500mg

Doctor's Notes
patient name: SHOULD NOT APPEAR
Follow up if no improvement.

Assessment
- Mild severity

Plan
- Rest
- Hydration

Red Flags
- Persistent high fever

Disclaimer
- For clinical use only; may contain transcription errors.
"""

            return _Msg(text)
    import core.langchain_pipeline as lp
    monkeypatch.setattr(lp, "ChatOpenAI", FakeChatOpenAI)
    return True
