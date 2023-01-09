import discord
from discord import Option
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = discord.Bot()

def gen_url(text):
    return "https://www.google.com/search?q="+text.replace(" ","+")

@bot.slash_command(description="google検索結果のURLを生成するよ(香辛料向け") 
async def googleurl(ctx: discord.ApplicationContext,text: Option(str, required=True, description="検索内容", )):
    await ctx.respond(f"「{text}」の検索結果\n{gen_url(text)}")

bot.run(TOKEN)