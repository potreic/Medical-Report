#Structure
``
Medical-Report/
│
├── bot.py                        # Entry point — main Discord bot script
│
├── config/
│   ├── config.py                  # API keys, paths, constants
│   └── prompts/                   # Prompt templates for LangChain
│       └── report_prompt.txt
│
├── cogs/                          # Discord command handlers (modular)
│   ├── __init__.py
│   └── consultation.py            # Handles audio upload & report generation
│
├── core/                          # Core processing logic
│   ├── __init__.py
│   ├── speech_to_text.py          # Whisper or Google Speech transcription
│   ├── report_generator.py        # LangChain structured report builder
│   ├── file_generator.py          # Generate .docx/.pdf from report
│   └── inventory_updater.py       # Optional: connect to hospital inventory DB/API
│
├── data/
│   ├── audio/                     # Temporarily stores uploaded audio
│   ├── transcripts/               # Raw text after transcription
│   └── reports/                   # Generated structured reports
│
├── requirements.txt               # All dependencies
│
├── .env                           # API keys (OpenAI, Discord, etc.)
│
└── README.md                      # Project documentation
``
