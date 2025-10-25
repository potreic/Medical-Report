# cogs/consultation.py
import os
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime
from core.speech_to_text import transcribe_audio
import os


class Consultation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_dir = os.getenv("TEMP_DIR", "data/audio")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore bot messages
        if message.author.bot:
            return

        # check if there are attachments
        if not message.attachments:
            return

        for attachment in message.attachments:
            # simple filter for audio files
            if attachment.filename.lower().endswith((".mp3", ".wav", ".m4a", ".ogg")):
                # create filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = f"{message.author.name}_{timestamp}_{attachment.filename}"
                save_path = os.path.join(self.audio_dir, safe_name)

                os.makedirs(self.audio_dir, exist_ok=True)

                # download and save
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(save_path, "wb") as f:
                                f.write(await resp.read())

                await message.channel.send(f"✅ Audio received and saved as `{safe_name}`.")
                print(f"Saved: {save_path}")
            else:
                await message.channel.send("⚠️ Please upload a valid audio file (.mp3, .wav, .m4a, .ogg).")

    @commands.command(name="transcribe")
    async def transcribe_command(self, ctx, *, filename: str = None):
        """
        Manually transcribe an audio file already saved in data/audio/
        Usage: !transcribe <filename>
        Example: !transcribe user_20251025_133000_audio.mp3
        """

        if not filename:
            await ctx.send("⚠️ Please specify the audio filename (from data/audio/).")
            return

        file_path = os.path.join("data", "audio", filename)

        if not os.path.exists(file_path):
            await ctx.send("❌ File not found.")
            return

        await ctx.send(f"🕓 Transcribing `{filename}`... this may take a moment.")

        try:
            text = await ctx.bot.loop.run_in_executor(None, transcribe_audio, file_path)

            # save transcript
            os.makedirs("data/transcripts", exist_ok=True)
            transcript_path = os.path.join("data", "transcripts", f"{filename}.txt")

            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(text)

            await ctx.send(f"✅ Transcription completed and saved as `{transcript_path}`")

        except Exception as e:
            await ctx.send(f"❌ Transcription failed: {str(e)}")

async def setup(bot):
    await bot.add_cog(Consultation(bot))
