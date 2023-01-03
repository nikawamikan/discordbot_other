import discord
import os


TOKEN = os.getenv("TOKEN")
bot = discord.Bot()

bot.run(TOKEN)