import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.scraper import (
    get_latest_posts,
    get_latest_rss_videos,
    load_sent_post_ids,
    save_sent_post_ids,
    save_video_id
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
VIDEO_CHANNEL_ID = int(os.getenv("VIDEO_CHANNEL_ID", "0"))
YT_CHANNEL_URL = os.getenv("YT_COMMUNITY_URL", "https://www.youtube.com/@MuseIndonesia")
FALLBACK_THUMBNAIL = "https://i.imgur.com/xlRZ7gH.jpg"  # Gambar default jika thumbnail tidak valid

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

@tasks.loop(seconds=60)
async def check_community():
    sent_post_ids = load_sent_post_ids()
    posts = get_latest_posts(YT_CHANNEL_URL)
    channel = bot.get_channel(CHANNEL_ID)

    for post in posts:
        if post["id"] not in sent_post_ids:
            embed = discord.Embed(
                description=post["text"] or "(Tanpa teks)",
                url=post["url"],
                color=discord.Color.blue()
            )
            embed.set_footer(text="Notifikasi komunitas oleh Waifu-chan 🥰")

            embed.set_image(url=post["thumbnail"] or FALLBACK_THUMBNAIL)

            if channel:
                await channel.send(embed=embed)
            sent_post_ids.append(post["id"])

    save_sent_post_ids(sent_post_ids)

@tasks.loop(seconds=60)
async def check_video():
    videos = get_latest_rss_videos()
    channel = bot.get_channel(VIDEO_CHANNEL_ID)

    for video in videos:
        embed = discord.Embed(
            title=video["title"],
            description=f"📅 {video['published']}",
            url=video["url"],
            color=discord.Color.red()
        )
        embed.set_author(name="Muse Indonesia", url=YT_CHANNEL_URL)
        embed.set_image(url=f"https://img.youtube.com/vi/{video['id']}/hqdefault.jpg")
        embed.set_footer(text="Notifikasi video oleh Waifu-chan ❤️")

        if channel:
            await channel.send(embed=embed)
        save_video_id(video["id"])

@bot.command()
async def cekpost(ctx):
    posts = get_latest_posts(YT_CHANNEL_URL, max_posts=1)
    post = posts[0] if posts else None

    if not post:
        await ctx.send("❌ Tidak ditemukan post.")
        return

    embed = discord.Embed(
        description=post["text"] or "(Tanpa teks)",
        url=post["url"],
        color=discord.Color.green()
    )
    embed.set_footer(text="Manual oleh Waifu-chan 😇")

    embed.set_image(url=post["thumbnail"] or FALLBACK_THUMBNAIL)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    check_community.start()
    check_video.start()

bot.run(TOKEN)
