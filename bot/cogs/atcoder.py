import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands, tasks
import datetime

ATCODER_URL = 'https://atcoder.jp/contests/'


def get_data():
    r = requests.get(ATCODER_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    elems = soup.find(
        'div', id='contest-table-upcoming').div.div.table.tbody.find_all("tr")
    return [Event(
        title=elem.contents[3].a.text,
        url='https://atcoder.jp'+elem.contents[3].a.attrs['href'],
        time=elem.find('time').text
    ) for elem in elems]


class Event:
    def __init__(self, title: str, url: str, time: str):
        self.title = title
        self.url = url
        self.time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S%z")


def notification_list_filter(events: list[Event]) -> list[Event]:
    date_format = "%Y%m%d%H"
    contest_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    contest_time_str = contest_time.strftime(date_format)
    return [v for v in events if v.time.strftime(date_format) == contest_time_str]


def get_embed(title: str, events: list[Event]):
    fields = [discord.EmbedField(
        name=f"{v.title}\n{v.time.strftime('%Y/%m/%d %H:%M')}",
        value=f"{v.url}\n."
    ) for v in events]
    embed = discord.Embed(
        title=title,
        color=0x00ff00,
        url=ATCODER_URL,
        fields=fields
    )
    return embed


class atcoder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        print("start atcoder init")
        self.bot = bot
        self.notification.start()

    @commands.slash_command(description="atcoderコンテスト予定")
    async def atcoder(
        self,
        ctx: discord.ApplicationContext,
    ):
        s = "〈〈今後のコンテスト予定〉〉"
        embed = get_embed(title=s, events=get_data())
        await ctx.respond(embed=embed)

    @tasks.loop(time=[datetime.time(i, 0, 0, 0) for i in range(24)])
    async def notification(self):
        data = notification_list_filter(get_data())
        if len(data) == 0:
            return
        embed = get_embed(title="1時間後に開催されるコンテスト", events=data)
        await self.channel.send(content=self.role.mention, embed=embed)

    @notification.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        self.channel: discord.TextChannel = self.bot.get_channel(
            1018523915695443978)
        self.role = self.channel.guild.get_role(1099670573409370162)


def setup(bot):
    bot.add_cog(atcoder(bot))
