# main.py

import discord
from discord.ext import commands
import requests
from datetime import datetime
import pytz
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def convert_to_wib(utc_time_str):
    try:
        utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_dt = pytz.utc.localize(utc_dt)
        wib_tz = pytz.timezone("Asia/Jakarta")
        wib_dt = utc_dt.astimezone(wib_tz)
        return wib_dt.strftime("%d %B %Y • %H:%M WIB")
    except Exception as e:
        print("Gagal konversi waktu:", e)
        return "Waktu tidak tersedia"

def get_valid_thumbnail(url):
    try:
        res = requests.get(url)
        if res.status_code == 200 and "image" in res.headers.get("content-type", ""):
            return url
        else:
            return "https://i.imgur.com/placeholder.png"
    except:
        return "https://i.imgur.com/placeholder.png"

@bot.command()
async def notify(ctx):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            video_data = json.load(f)
    except Exception as e:
        await ctx.send("Gagal membaca data video.")
        print("Error:", e)
        return

    formatted_time = convert_to_wib(video_data.get("publishedAt", ""))
    thumbnail_url = get_valid_thumbnail(video_data.get("thumbnail", ""))

    embed = discord.Embed(
        title=video_data.get("title", "Judul tidak tersedia"),
        url=video_data.get("link", ""),
        description=f"📺 Channel: {video_data.get('channel', 'Tidak diketahui')}\n🕒 {formatted_time}",
        color=discord.Color.purple()
    )
    embed.set_image(url=thumbnail_url)
    embed.set_footer(text="Notifikasi Waifu-chan")

    await ctx.send(embed=embed)

bot.run("your_bot_token")
