import os
from docx import Document
from cogs.consultation import save_tidy_docx

def test_save_tidy_docx_creates_file_with_sections(temp_dirs):
    report_path = os.path.join(temp_dirs["reports"], "user_20250101_120000_audio.docx")
    # konten ringkas utk semua header
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
    # buka dan cek beberapa teks utama
    doc = Document(report_path)
    full = "\n".join(p.text for p in doc.paragraphs)
    assert "Medical Consultation Report" in full
    assert "Patient Name: Jane" in full
    assert "Date of Consultation:" in full
