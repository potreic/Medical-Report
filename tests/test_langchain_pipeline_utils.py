from core.langchain_pipeline import (
    _strip_llm_special_tokens, _censor_patient_lines, _ensure_section_order
)

def test_strip_llm_special_tokens_removes_control_markers():
    s = "Hello <|begin_of_sentence|> world </think> <think> test"
    out = _strip_llm_special_tokens(s)
    assert "<|" not in out and "<think>" not in out and "</think>" not in out

def test_censor_patient_lines_filters_identifiers():
    inp = "Patient Name: John\nAge: 30\nSymptoms\n- Cough"
    out = _censor_patient_lines(inp)
    assert "Patient Name" not in out and "Age:" not in out
    assert "Symptoms" in out

def test_ensure_section_order_inserts_placeholders_and_normalizes():
    # input hanya sebagian dan urutan acak
    inp = "Assessment\n- Mild\nSymptoms\n- Fever"
    out = _ensure_section_order(inp)
    # Semua header harus ada dan 'Symptoms' duluan
    expected_headers = [
        "Symptoms","Diagnosis","Prescription / Treatment Plan",
        "Doctor's Notes","Assessment","Plan","Red Flags","Disclaimer"
    ]
    for h in expected_headers:
        assert f"\n{h}\n" in "\n" + out + "\n"
    # Ada placeholder bila kosong
    assert "- None reported." in out
