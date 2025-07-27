import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import pytz

# 🔧 Inisialisasi
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
VIDEO_CHANNEL_ID = int(os.getenv("VIDEO_CHANNEL_ID", "0"))
YT_CHANNEL_URL = os.getenv("YT_COMMUNITY_URL", "https://www.youtube.com/@MuseIndonesia")
start_time = datetime.utcnow()

# 🔌 Setup Intents & Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # penting untuk kick/move
bot = commands.Bot(command_prefix="~", intents=intents)

# 🧩 Import Setup Command Modular
from commands.peraturan import setup_peraturan_commands
from commands.admin_owner import setup_admin_owner_commands
from commands.botinfo import setup_botinfo_commands
from commands.general_command import setup_general_commands
from utils.scraper import (
    get_latest_posts, get_latest_rss_videos,
    load_sent_post_ids, save_sent_post_ids,
    load_sent_video_ids, save_sent_video_ids
)

# 🧠 Daftarkan Semua Command
setup_peraturan_commands(bot)
setup_admin_owner_commands(bot, CHANNEL_ID, CHANNEL_ID, YT_CHANNEL_URL, [])
setup_botinfo_commands(bot)
setup_general_commands(bot)

# 🔁 Loop Komunitas
@tasks.loop(seconds=30)
async def check_community():
    sent_post_ids = load_sent_post_ids()
    new_posts = get_latest_posts(YT_CHANNEL_URL, max_posts=5)
    channel = bot.get_channel(CHANNEL_ID)

    if not new_posts or not channel:
        return

    for post in new_posts:
        if post["id"] in sent_post_ids:
            continue

        embed = discord.Embed(
            title="Post Komunitas Baru",
            url=post["url"],
            description=f"📝 {post['text'] or '(Tanpa teks)'}\n📅 {post['timestamp']}",
            color=discord.Color.blue()
        )
        embed.set_author(name="Muse Indonesia", url=YT_CHANNEL_URL)
        embed.set_footer(text="Notifikasi komunitas oleh Waifu-chan❤️")

        await channel.send(embed=embed)
        sent_post_ids.append(post["id"])

    save_sent_post_ids(sent_post_ids)

# 🔁 Loop Video Otomatis
@tasks.loop(seconds=30)
async def check_video():
    sent_video_ids = load_sent_video_ids()
    new_videos = get_latest_rss_videos()
    channel = bot.get_channel(VIDEO_CHANNEL_ID)

    if not new_videos or not channel:
        return

    for video in new_videos:
        if video["id"] in sent_video_ids:
            continue

        # Parsing waktu dari RSS (UTC format)
        published_dt = datetime.strptime(video["published"], "%Y-%m-%dT%H:%M:%S%z")

        # Konversi ke zona waktu WIB
        local_tz = pytz.timezone("Asia/Jakarta")
        published_local = published_dt.astimezone(local_tz)

        # Format tanggal dan jam
        tanggal = published_local.strftime("%d %B %Y")  # Contoh: 27 Juli 2025
        jam = published_local.strftime("%H:%M:%S")      # Contoh: 10:45:12

        embed = discord.Embed(
            title=video["title"],
            url=video["url"],
            description=f"📅 {tanggal}\n⏰ {jam} WIB",
            color=discord.Color.red()
        )
        embed.set_author(name="Muse Indonesia", url=YT_CHANNEL_URL)
        embed.set_image(url=f"https://img.youtube.com/vi/{video['id']}/hqdefault.jpg")
        embed.set_footer(text="Notifikasi video oleh Waifu-chan❤️")

        await channel.send(embed=embed)
        sent_video_ids.append(video["id"])

    save_sent_video_ids(sent_video_ids)

# 🕒 Tunggu Bot Siap Sebelum Mulai Loop
@check_community.before_loop
async def before_community():
    await bot.wait_until_ready()

@check_video.before_loop
async def before_video():
    await bot.wait_until_ready()

# 🚀 Bot Siap Jalan
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"🧠 Commands aktif: {[cmd.name for cmd in bot.commands]}")
    check_community.start()
    check_video.start()

# 🧠 Jalankan Bot
bot.run(TOKEN)
