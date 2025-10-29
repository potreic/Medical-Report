from core.langchain_pipeline import generate_medical_report

def test_generate_medical_report_normalizes_and_censors(fake_llm):
    transcript = "Patient says coughing and fever for 2 days."
    out = generate_medical_report(transcript)
    # Semua header ada
    for h in [
        "Symptoms","Diagnosis","Prescription / Treatment Plan",
        "Doctor's Notes","Assessment","Plan","Red Flags","Disclaimer"
    ]:
        assert f"\n{h}\n" in "\n" + out + "\n"
    # Token kontrol dibersihkan
    assert "<|" not in out and "patient name:" not in out.lower()
    # Bullet menggunakan '-' (bukan '•')
    assert "•" not in out
