import re
from cogs.consultation import Consultation, _canonical_section, SECTION_ALIASES

def test_parse_patient_info_multiple_formats():
    p = Consultation._parse_patient_info('name="Athaya Kusuma" id=P-00123')
    assert p == ("Athaya Kusuma", "P-00123")

    p2 = Consultation._parse_patient_info('Nama: "Budi"; ID: X-77')
    assert p2 == ("Budi", "X-77")

    p3 = Consultation._parse_patient_info('!patient "Sinta" P-9')
    # via cmd format fallback di cmd handler; di sini _parse bisa gagal -> (None,None)
    assert p3 == (None, None)

def test_canonical_section_aliases_basic():
    sections = [
        "Symptoms","Diagnosis","Prescription / Treatment Plan",
        "Doctor's Notes","Assessment","Plan","Red Flags","Disclaimer"
    ]
    assert _canonical_section("dx", sections) == "Diagnosis"
    assert _canonical_section("treatment plan", sections) == "Prescription / Treatment Plan"
    assert _canonical_section("Doctor's notes:", sections) == "Doctor's Notes"
    assert _canonical_section("warning signs", sections) == "Red Flags"
