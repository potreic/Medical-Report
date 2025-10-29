import os
from docx import Document
from cogs.consultation import save_tidy_docx

def test_save_tidy_docx_uses_fallback_date_when_filename_has_no_timestamp(temp_dirs):
    # nama file TANPA pola _YYYYMMDD_HHMMSS_
    report_path = os.path.join(temp_dirs["reports"], "user_audio.docx")

    # konten minimal mencakup semua header agar renderer berjalan mulus
    text = "\n".join([
        "Symptoms","- Fever",
        "Diagnosis","- Viral",
        "Prescription / Treatment Plan","- Paracetamol",
        "Doctor's Notes","- Observe",
        "Assessment","- Mild",
        "Plan","- Rest",
        "Red Flags","- None",
        "Disclaimer","- For clinical use only"
    ])

    save_tidy_docx(
        report_text=text,
        report_path=report_path,
        author_name="Tester",
        patient_name="Jane",
        patient_id="P-1"
    )

    assert os.path.exists(report_path)

    # verifikasi fallback tanggal
    doc = Document(report_path)
    # gabungkan semua paragraf untuk memudahkan pencarian
    full = "\n".join(p.text for p in doc.paragraphs)
    assert "Medical Consultation Report" in full
    assert "Patient Name: Jane" in full
    assert "Date of Consultation: [Date not available]" in full
