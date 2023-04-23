import requests
from bs4 import BeautifulSoup
import discord
from discord import Option
from discord.ext import commands



class atcoder(commands.Cog):
    def __init__(self, bot):
        print("start atcoder init")
        self.bot = bot

    def get_data():
        res=[]
        r = requests.get('https://atcoder.jp/contests/')
        soup = BeautifulSoup(r.content, "html.parser")
        elems = soup.find('div',id='contest-table-upcoming').div.div.table.tbody.find_all("tr")
        for elem in elems:
            p={}
            p['title']=(elem.contents[3].a.text)
            p['url']=('https://atcoder.jp'+elem.contents[3].a.attrs['href'])
            p['time']=(elem.find('time').text)
            res.append(p)
        return res

    @commands.slash_command(description="atcoderコンテスト予定") 
    async def atcoder(
        self,
        ctx: discord.ApplicationContext,
        ):
            contests=atcoder.get_data()
            embed=discord.Embed(
                title=f"〈〈今後のコンテスト予定〉〉",
                color=0x00ff00,
                url=f"https://atcoder.jp/contests/"
                
            )
            for data in contests:  
                embed.add_field(name=data['title']+'\n'+data['time'].split()[0],value=data['url']+'\n.',inline=False)
            await ctx.respond(embed=embed)
        



def setup(bot):
    bot.add_cog(atcoder(bot))
