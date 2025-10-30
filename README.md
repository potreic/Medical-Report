# 🩺 Medical Report Generator
A modular Python-based system for **automating the generation and structuring of medical reports** using advanced language models.  Built with **LangChain**, **DeepSeek**, and a modular core architecture, this project turns raw medical data or transcriptions into clean, clinically styled `.docx` reports.

## ✨ Features
- 🧠 **AI-Powered Report Generation** — Uses a LangChain pipeline to interact with DeepSeek for structured medical summaries.  
- 🧩 **Modular Architecture** — Organized into `core/`, `config/`, and `cogs/` for easy maintenance and scaling.  
- 📄 **DOCX Output Renderer** — Automatically produces formatted `.docx` reports from model outputs.  
- ⚙️ **Configurable Settings** — Easy environment setup via `.env` and centralized configuration management.  
- 💬 **Bot-Ready Interface** — Includes a bot interface (`bot.py`) that can integrate with chat or API endpoints.


## 🏗️ Project Structure
```
Medical-Report/
├── cogs/
│   └── consultation.py
├── config/
│   └── settings.py
├── core/
│   ├── langchain_pipeline.py
│   └── speech_to_text.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_consultation_helpers.py
│   ├── test_docx_renderer.py
│   ├── test_docx_renderer_no_date.py
│   ├── test_generate_medical_report_functional.py
│   ├── test_langchain_pipeline_utils.py
│   └── test_speech_to_text_errors.py
├── .env.example
├── bot.py
└── requirements.txt

```

## 🚀 Set Up and Run
### 1️⃣ Clone the repository
```
git clone https://github.com/potreic/Medical-Report.git
cd Medical-Report
```
### 2️⃣ Set up a virtual environment
```
python -m venv venv
source venv/bin/activate   # On Linux / macOS
venv\Scripts\activate      # On Windows
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Configure environment variables
```
DISCORD_TOKEN=put-your-discord-bot-token-here
ASSEMBLYAI_API_KEY=put-your-assemblyai-key-here
OPENROUTER_API_KEY=put-your-openrouter-api-key-here
```
### 5️⃣ Run!
```
python bot.py
```

## 👩‍💻 Demo
### 1️⃣ Send Data Patient
  <img src="https://github.com/potreic/Medical-Report/blob/main/assets/IMG_3855.gif?raw=true" 
       alt="Medical Report Demo 1" 
       style="width:320px; aspect-ratio:4/5; object-fit:cover; border-radius:12px; margin:8px;" />

### 2️⃣ Send Audio Consultation
  <img src="https://github.com/potreic/Medical-Report/blob/main/assets/IMG_3858.gif?raw=true" 
       alt="Medical Report Demo 2" 
       style="width:320px; aspect-ratio:4/5; object-fit:cover; border-radius:12px; margin:8px;" />

## 🤼 Credit:
1. Athaya Harmana Putri: testing and quality engineer
2. Nibroos Haryanto: system engineer and logic orchestration

##
<div align="center">
Crafted with 💚 by Rore & Thaya | Intended for NLP's project
</div>
