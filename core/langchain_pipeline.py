# core/langchain_pipeline.py (cleaner structure for DOCX rendering + more tolerant header regex)
from __future__ import annotations
import re
from typing import List
from config.settings import OPENROUTER_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Target sections expected by the DOCX renderer
SECTIONS: List[str] = [
    "Symptoms",
    "Diagnosis",
    "Prescription / Treatment Plan",
    "Doctor's Notes",
    "Assessment",
    "Plan",
    "Red Flags",
    "Disclaimer",
]

_CENSOR_PATTERNS = [
    r"^\s*(patient\s*name|nama\s*pasien)\s*[:=].*$",
    r"^\s*(patient\s*id|id\s*pasien|mrn|rekam\s*medis)\s*[:=].*$",
    r"^\s*(dob|tanggal\s*lahir|age|umur)\s*[:=].*$",
    r"^\s*(date\s*of\s*consultation|tanggal\s*konsultasi)\s*[:=].*$",
    r"^\s*(alamat|address|phone|telepon)\s*[:=].*$",
]

def _strip_markdown(text: str) -> str:
    """Remove Markdown artifacts (#, **, code fences) and trim whitespace."""
    text = re.sub(r"```[\s\S]*?```", lambda m: m.group(0).strip("`\n"), text)  # unwrap fences
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)  # remove # headers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # italics
    return text.strip()


def _strip_llm_special_tokens(text: str) -> str:
    """
    Remove model control tokens such as:
      - <|begin_of_sentence|>, <|end_of_text|>
      - <｜begin▁of▁sentence｜> (unicode bars + underscores)
      - optional leading/trailing dots and spaces around the token
      - <think> ... </think> wrappers (defensive)
    """
    # Remove tokens enclosed by <|...|> or <｜...｜>, allow any inner text (non-greedy)
    text = re.sub(r"[.\s]*<\s*[|｜]\s*[^|｜>]+?\s*[|｜]\s*>[.\s]*", "", text)
    # Remove <think> wrappers if a model emits them
    text = re.sub(r"</?think>", "", text, flags=re.IGNORECASE)
    return text

def _censor_patient_lines(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    kept = []
    for ln in lines:
        if any(re.search(p, ln, flags=re.IGNORECASE) for p in _CENSOR_PATTERNS):
            continue
        kept.append(ln)
    return "\n".join(kept).strip()

def _ensure_section_order(text: str) -> str:
    """Best-effort normalize to our exact section headers and order.
    If a section is missing, insert a placeholder line.
    """
    # Build tolerant pattern for exact headers (allow trailing colon and flexible ' / ')
    def _pattern_for(h: str) -> str:
        # escape then relax the slash spacing
        pat = re.escape(h)
        pat = pat.replace(r"\ /\/\ ", r"\s*/\s*").replace(r"\/", r"\s*/\s*")
        return pat

    header_re = re.compile(
        r"^(%s)\s*:?\s*$" % "|".join([_pattern_for(s) for s in SECTIONS]),
        re.IGNORECASE
    )

    current = None
    buckets = {s: [] for s in SECTIONS}

    for raw in text.splitlines():
        # NEW: strip special tokens BEFORE matching headers / collecting lines
        line = _strip_llm_special_tokens(raw.strip())
        if not line:
            continue
        m = header_re.match(line)
        if m:
            # canonical header case
            target = m.group(1)
            canonical = next(s for s in SECTIONS if re.fullmatch(_pattern_for(s), target, flags=re.IGNORECASE))
            current = canonical
            continue
        if current is None:
            current = "Doctor's Notes"
        buckets[current].append(line)

    # Compose output
    out_lines: List[str] = []
    for s in SECTIONS:
        out_lines.append(s)
        content = buckets.get(s) or []
        if not content:
            out_lines.append("- None reported.")
        else:
            for ln in content:
                # NEW: per-line cleanup too (defensive)
                ln = _strip_llm_special_tokens(ln)
                if re.match(r"^[\-•]\s+", ln):
                    ln = re.sub(r"^[\-•]\s+", "- ", ln)
                out_lines.append(ln)
        out_lines.append("")
    return "\n".join(out_lines).strip() + "\n"

def generate_medical_report(transcribed_text: str) -> str:
    """
    Takes doctor–patient consultation text and generates
    a structured medical report using DeepSeek via OpenRouter API,
    formatted to be DOCX-friendly (no Markdown symbols) and aligned with our renderer.
    """
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3.1:free",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
    )

    # IMPORTANT: exact headers (no markdown), concise hyphen bullets, no patient identifiers
    prompt_template = ChatPromptTemplate.from_template(
        """
        You are a professional medical scribe. Convert the doctor–patient consultation
        into a concise, objective medical report. Follow these STRICT rules:

        1) Output PLAIN TEXT only. Do NOT use Markdown (#, **, bullets like •). Bullets MUST be hyphens: "- ".
        2) Use EXACTLY these section headers, each on its own line (no colon, no numbering):
           Symptoms
           Diagnosis
           Prescription / Treatment Plan
           Doctor's Notes
           Assessment
           Plan
           Red Flags
           Disclaimer
        3) After each header, provide 1–8 short bullet points or brief lines. Keep it clinical and verifiable.
        4) DO NOT include patient identifiers (name, ID/MRN, DOB/age, phone, address) or dates.
        5) The Disclaimer section must be a single line about potential transcription errors and for clinical use only.

        Transcript:
        {transcript}
        """
    )

    messages = prompt_template.format_messages(transcript=transcribed_text)
    parser = StrOutputParser()
    response = llm.invoke(messages)
    raw = parser.parse(response.content)

    # Normalize to the exact structure the DOCX renderer expects
    cleaned = _strip_markdown(raw)
    cleaned = _strip_llm_special_tokens(cleaned)  # NEW: remove <|...|> / <｜...｜> tokens
    cleaned = _censor_patient_lines(cleaned)
    normalized = _ensure_section_order(cleaned)
    return normalized
