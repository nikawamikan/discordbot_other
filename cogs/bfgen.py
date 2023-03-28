import discord
from math import sqrt
from discord import Option
from discord.ext import commands

class bf_gen(commands.Cog):
    def __init__(self, bot):
        print("start bfgen init")
        self.bot = bot

    def gen_bf(s:str):
        res=">>+++++[<+++++>-]<[<++++>-]"
        cur=100
        for c in s:
            n=int(sqrt(abs(cur-ord(c))))
            a="-"
            if ord(c)-cur>0:a="+"
            res+="+"*n+"[<"+a*n+">-]<"+a*(abs(cur-ord(c))-n*n)+".>"
            cur=ord(c)
        return "```brainfuck\n"+res+"\n```"

    @commands.slash_command(description="入力文字列出力brainf**kコード出力discordbot") 
    async def bf(
        self,
        ctx: discord.ApplicationContext,
        text: Option(str, required=True, description="入力文字列(A~z)", )
        ):
            await ctx.respond(bf_gen.gen_bf(text))


def setup(bot):
    bot.add_cog(bf_gen(bot))