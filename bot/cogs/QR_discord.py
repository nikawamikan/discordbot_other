import pyshorteners
import qrcode

import discord
from discord import Option
from discord.ext import commands

s = pyshorteners.Shortener()


def gen_QR(url):
    img = qrcode.make(url)
    img.save('QR.png')


class QR(commands.Cog):
    def __init__(self, bot):
        print("start QR init")
        self.bot = bot

    @commands.slash_command(description="URLからQRを生成するよ")
    async def qr(self, ctx: discord.ApplicationContext, text: Option(str, required=True, description="URL", )):
        gen_QR(s.tinyurl.short(text))
        print(s.tinyurl.short(text))
        await ctx.respond(text, file=discord.File("QR.png"))


def setup(bot):
    bot.add_cog(QR(bot))
