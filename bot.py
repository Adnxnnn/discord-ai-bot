import discord
from dotenv import load_dotenv
load_dotenv()  # loads secrets from .env if present
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


# ====== EVENTS ======
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    print(f"Bot is online as {bot.user}")


# ====== SLASH COMMAND ======
@bot.tree.command(name="chat", description="Chat with AI (Gemini)")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()

    try:
        response = model.generate_content(message)
        await interaction.followup.send(response.text)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")


# ====== RUN ======
bot.run(DISCORD_TOKEN)
