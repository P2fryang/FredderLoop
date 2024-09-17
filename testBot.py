import discord
from discord.ext import commands
from discord import app_commands
from config import BOT_TOKEN

# Create a bot with default intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("Commands synced")

# Define a command that responds with "Hello, World!"
@bot.tree.command(name='hello', description="Replies")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f", World! {interaction.user.mention}")

bot.run(BOT_TOKEN)

