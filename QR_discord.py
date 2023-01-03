import discord
import pyshorteners
import qrcode
from discord import Option
import os
from dotenv import load_dotenv

s=pyshorteners.Shortener()
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = discord.Bot()

def gen_QR(url):
    img =qrcode.make(url)
    img.save('QR.png')

@bot.slash_command(description="URLからQRを生成するよ") 
async def qr(ctx: discord.ApplicationContext,text: Option(str, required=True, description="URL", )):
    gen_QR(s.tinyurl.short(text))
    print(s.tinyurl.short(text))
    await ctx.respond(text,file=discord.File("QR.png"))

bot.run(TOKEN)