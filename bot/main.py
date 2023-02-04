import discord
from discord.ext import commands
import os
from model.genshin_photo import init_table, get_last_date, add_photo_list, GenshinPhoto, delete_photo
import re
from datetime import datetime
import hashlib
import aiohttp
import aiofiles

URL_CHARS = list(
    "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-_")
CHAR_LENGTH = len(URL_CHARS)


def get_file_name(url: str, extension: str = ".png"):
    result = ""
    h = int(hashlib.md5(url.encode()).hexdigest(), 16)
    for _ in range(22):
        result += URL_CHARS[h % CHAR_LENGTH]
        h = h >> 6
    return result + extension


SIZE_DICT = {"fullhd": 1920, "thumbnail": 854}


async def resize_photo_and_get_filename(url: str, width: int, height: int):
    file_name = get_file_name(url)
    for v in ["fullhd", "thumbnail", "original"]:
        tmp = url
        if v in SIZE_DICT:
            tmp = f"{url}?width={SIZE_DICT[v]}&height={SIZE_DICT[v]*height//width}"
        async with aiohttp.request("get", tmp) as response:
            if response.status == 200:
                async with aiofiles.open(f"images/{v}/{file_name}", "wb") as f:
                    f.write(await response.read())
    return file_name


init_table()

PATTERN = re.compile(r"https://.+png")

TOKEN = os.getenv("TOKEN")
GUILDS = os.getenv("GUILDS")
INTENTS = discord.Intents.all()

print(GUILDS)
bot = commands.Bot(
    debug_guilds=[int(v) for v in GUILDS.split(",")],
    intents=INTENTS
)

genshin_photo = int(os.getenv("GENSHIN_PHOTO"))


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")
    channel: discord.TextChannel = await bot.fetch_channel(genshin_photo)
    messages = await channel.history(limit=None).flatten()
    genshin_photos: list[GenshinPhoto] = []
    for message in messages:
        for attachment in message.attachments:
            url = attachment.url.replace(
                "https://cdn.discordapp.com", "https://media.discordapp.net")
            genshin_photos.append(
                GenshinPhoto(
                    user_id=message.author.id,
                    url=url,
                    width=attachment.width,
                    height=attachment.height,
                    message_id=message.id,
                    date=message.created_at,
                    filename=await resize_photo_and_get_filename(
                        url, attachment.width, attachment.height)
                )
            )
    if len(genshin_photos) > 0:
        add_photo_list(genshin_photos=genshin_photos)


@bot.listen('on_message')
async def genshin_photo_deamon(message: discord.Message):
    if message.channel.id == genshin_photo and not message.author.bot:
        genshin_photos: list[GenshinPhoto] = []
        for attachment in message.attachments:
            url = attachment.url.replace(
                "https://cdn.discordapp.com", "https://media.discordapp.net")
            genshin_photos.append(
                GenshinPhoto(
                    user_id=message.author.id,
                    url=url,
                    width=attachment.width,
                    height=attachment.height,
                    message_id=message.id,
                    date=message.created_at,
                    filename=await resize_photo_and_get_filename(
                        url, attachment.width, attachment.height)
                )
            )
        print(len(genshin_photos))
        if len(genshin_photos) > 0:
            add_photo_list(genshin_photos=genshin_photos)


@bot.listen("on_message_delete")
async def genshin_photo_delete(message: discord.Message):
    if message.channel.id == genshin_photo and not message.author.bot:
        print(f"message id: {message.id} delete")
        delete_photo(message_id=message.id)


bot.load_extensions(
    "cogs.PNR_discord",
    "cogs.QR_discord",
    "cogs.googleserch",
    store=False
)

bot.run(TOKEN)
