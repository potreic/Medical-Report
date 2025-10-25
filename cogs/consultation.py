import os
import aiohttp
from datetime import datetime
import discord
import re
from discord.ext import commands
from datetime import datetime
from config.settings import TEMP_DIR, REPORT_DIR
from core.speech_to_text import transcribe_audio
from core.langchain_pipeline import generate_medical_report
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


class Consultation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_dir = TEMP_DIR
        self.transcript_dir = "data/transcripts"
        self.report_dir = REPORT_DIR

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Automatically saves uploaded audio files into data/audio/"""
        if message.author.bot or not message.attachments:
            return

        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".mp3", ".wav", ".m4a", ".ogg")):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = f"{message.author.name}_{timestamp}_{attachment.filename}"
                save_path = os.path.join(self.audio_dir, safe_name)

                os.makedirs(self.audio_dir, exist_ok=True)

                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(save_path, "wb") as f:
                                f.write(await resp.read())

                await message.channel.send(f"✅ Audio received and saved as `{safe_name}`.")
                print(f"[INFO] Saved audio: {save_path}")
            else:
                await message.channel.send(
                    "⚠️ Please upload a valid audio file (.mp3, .wav, .m4a, .ogg)."
                )


    @commands.command(name="transcribe")
    async def transcribe_command(self, ctx, *, filename: str = None):
        """
        Transcribe an audio file and generate a structured medical report (.docx)
        Usage: !transcribe <filename>
        Example: !transcribe user_20251025_133000_audio.mp3
        """
        if not filename:
            await ctx.send("⚠️ Please specify the audio filename (from data/audio/).")
            return

        file_path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(file_path):
            await ctx.send("❌ File not found.")
            return

        await ctx.send(f"🕓 Transcribing `{filename}`... please wait.")

        try:
            text = await ctx.bot.loop.run_in_executor(None, transcribe_audio, file_path)

            os.makedirs(self.transcript_dir, exist_ok=True)
            transcript_path = os.path.join(self.transcript_dir, f"{filename}.txt")
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(text)

            await ctx.send("✅ Transcription completed. Generating medical report...")

            report_text = await ctx.bot.loop.run_in_executor(
                None, generate_medical_report, text
            )

            os.makedirs(self.report_dir, exist_ok=True)
            report_path = os.path.join(self.report_dir, f"{filename}.docx")
            save_tidy_docx(report_text, report_path, ctx.author.name)

            await ctx.send("📄 Report generated successfully!", file=discord.File(report_path))

        except Exception as e:
            await ctx.send(f"❌ Process failed: {str(e)}")
            raise e

def save_tidy_docx(report_text: str, report_path: str, author_name: str = "Unknown"):
    """
    Generate a clean, professional medical report in Times New Roman format.
    Automatically extracts consultation date from filename (YYYYMMDD).
    """

    # --- Extract date from filename if possible ---
    # Expecting filenames like: user_20251025_152535_voice-message.ogg
    match = re.search(r"(\d{8})_\d{6}", report_path)
    if match:
        raw_date = match.group(1)
        try:
            consultation_date = datetime.strptime(raw_date, "%Y%m%d").strftime("%d %B %Y")
        except ValueError:
            consultation_date = "[Date not available]"
    else:
        consultation_date = "[Date not available]"

    doc = Document()

    # Global font
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    # Title
    title = doc.add_paragraph("Medical Consultation Report")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.runs[0]
    title_run.font.bold = True
    title_run.font.size = Pt(14)
    doc.add_paragraph()  # spacing

    # Section list to detect headers
    sections = [
        "Patient Information",
        "Symptoms",
        "Diagnosis",
        "Prescription / Treatment Plan",
        "Doctor's Notes",
    ]

    # Prepare lines
    lines = [line.strip() for line in report_text.splitlines() if line.strip()]
    inserted_date = False  # to prevent multiple date insertions

    for line in lines:
        # Section titles
        if any(line.lower().startswith(s.lower()) for s in sections):
            p = doc.add_paragraph(line)
            p.runs[0].font.bold = True
            doc.add_paragraph()
            current_section = line

            if "Patient Information" in line and not inserted_date:
                doc.add_paragraph(f"Date of Consultation: {consultation_date}")
                inserted_date = True

        # Subheaders like "Medications:" or "Non-pharmacological Recommendations:"
        elif line.lower().startswith(("medications", "non-pharmacological")):
            p = doc.add_paragraph(line)
            p.runs[0].font.bold = True

        # Disclaimer
        elif "disclaimer" in line.lower():
            doc.add_paragraph()
            disclaimer = doc.add_paragraph(line)
            disclaimer.alignment = WD_ALIGN_PARAGRAPH.LEFT
            disclaimer.runs[0].font.size = Pt(10)
            disclaimer.runs[0].italic = True

        # Normal text
        else:
            doc.add_paragraph(line)

    doc.add_paragraph()
    doc.save(report_path)

async def setup(bot):
    await bot.add_cog(Consultation(bot))
