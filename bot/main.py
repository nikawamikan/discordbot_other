import discord
from discord.ext import commands
import os


TOKEN = os.getenv("TOKEN")
GUILDS = os.getenv("GUILDS")
intents = discord.Intents.default()

print(GUILDS)
bot = commands.Bot(
    debug_guilds=[int(v) for v in GUILDS.split(",")],
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


bot.load_extensions(
    "cogs.PNR_discord",
    "cogs.QR_discord",
    "cogs.googleserch",
    store=False
)

bot.run(TOKEN)
