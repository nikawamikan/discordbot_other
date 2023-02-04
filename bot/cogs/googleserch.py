import discord
from discord import Option
from discord.ext import commands


class GoogleSearch(commands.Cog):
    def __init__(self, bot):
        print("start GoogleSearch init")
        self.bot = bot

    def gen_url(text):
        return "https://www.google.com/search?q="+text.replace(" ", "+")

    @commands.slash_command(description="google検索結果のURLを生成するよ(香辛料向け")
    async def googleurl(
        self,
        ctx: discord.ApplicationContext,
        text: Option(str, required=True, description="検索内容", )
    ):
        await ctx.respond(f"「{text}」の検索結果\n{GoogleSearch.gen_url(text)}")


def setup(bot):
    bot.add_cog(GoogleSearch(bot))
