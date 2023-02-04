import discord
from discord.ext import commands
import os
from model.genshin_photo import init_table, get_last_date, add_photo_list, GenshinPhoto, delete_photo
import re
from datetime import datetime
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
        for url in [v.url for v in message.attachments]:
            genshin_photos.append(
                GenshinPhoto(
                    user_id=message.author.id,
                    url=url,
                    date=message.created_at,
                    message_id=message.id,
                )
            )
    if len(genshin_photos) > 0:
        add_photo_list(genshin_photos=genshin_photos)


@bot.listen('on_message')
async def genshin_photo_deamon(message: discord.Message):
    if message.channel.id == genshin_photo and not message.author.bot:
        genshin_photos: list[GenshinPhoto] = []
        for url in [v.url for v in message.attachments]:
            genshin_photos.append(
                GenshinPhoto(
                    user_id=message.author.id,
                    url=url,
                    date=message.created_at,
                    message_id=message.id
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
