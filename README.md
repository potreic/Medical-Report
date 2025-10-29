# 🩺 Medical Report Generator
A modular Python-based system for **automating the generation and structuring of medical reports** using advanced language models.  
Built with **LangChain**, **DeepSeek**, and a modular core architecture, this project turns raw medical data or transcriptions into clean, clinically styled `.docx` reports.

## ✨ Features
- 🧠 **AI-Powered Report Generation** — Uses a LangChain pipeline to interact with DeepSeek or other LLMs for structured medical summaries.  
- 🧩 **Modular Architecture** — Organized into `core/`, `config/`, and `cogs/` for easy maintenance and scaling.  
- 📄 **DOCX Output Renderer** — Automatically produces formatted `.docx` reports from model outputs.  
- ⚙️ **Configurable Settings** — Easy environment setup via `.env` and centralized configuration management.  
- 💬 **Bot-Ready Interface** — Includes a bot interface (`bot.py`) that can integrate with chat or API endpoints.


## 🏗️ Project Structure
```
place holder report structurw
```

## 🚀 SetUp and Run
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



## 🤼 Credit:
1. Athaya Harmana Putri: testing and quality engineer
2. Nibroos Haryanto: system engineer and logic orchestration

##
<div align="center">
Crafted with 💚 by Rore & Thaya | Intended for NLP's project
</div>
