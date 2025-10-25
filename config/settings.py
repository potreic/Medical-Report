import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

TEMP_DIR = os.getenv("TEMP_DIR", "data/audio")
REPORT_DIR = os.getenv("REPORT_DIR", "data/reports")