import discord
from math import sqrt
from discord import Option
from discord.ext import commands
import requests, json

class Seichi(commands.Cog):
    def __init__(self, bot):
        print("start seichi init")
        self.bot = bot
    
    def get_data(id):
        res=requests.get("https://api.conarin.com/seichi/ranking/players/"+id)
        return json.loads(res.text)

    @commands.slash_command(description="整地鯖info") 
    async def seichi(
        self,
        ctx: discord.ApplicationContext,
        mcid : Option(str, required=True, description="MCID", )
        ):
            data=Seichi.get_data(mcid)
            if('error' in data):
                await ctx.respond("誤った入力です。")
            else:
                embed=discord.Embed(
                    title=f"[Lv{data['levels']['seichi']['level']}☆{data['levels']['seichi']['starLevel']}] {data['player']['name']} ",
                    color=0x00ff00,
                    url=f"https://seichi.conarin.com/ranking/players/{mcid}"
                )
                embed.add_field(name='ランキング',value='{:,}'.format(int(data['ranks'][0]['rank'])))
                embed.add_field(name='整地量',value='{:,}'.format(int(data['ranks'][0]['value'])))
                embed.add_field(name='建築レベル',value=data['levels']['build']['level'])
                embed.set_thumbnail(url=f"https://crafatar.com/renders/head/{data['player']['uuid']}")
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Seichi(bot))