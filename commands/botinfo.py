from discord.ext import commands
import discord
from datetime import datetime
start_time = datetime.utcnow()


def setup_botinfo_commands(bot):

    @bot.command(name="botinfo")
    async def botinfo(ctx):
        import platform
        uptime = datetime.utcnow() - start_time

        embed = discord.Embed(
            title="🤖 Info Waifu-chan",
            description="Bot anime-themed untuk notifikasi & interaksi server.",
            color=discord.Color.pink()
        )
        embed.add_field(name="🆔 Bot ID", value=str(bot.user.id))
        embed.add_field(name="📛 Nama", value=bot.user.name)
        embed.add_field(name="⏱️ Uptime", value=str(uptime).split('.')[0])
        embed.add_field(name="⚙️ Python", value=platform.python_version())
        embed.add_field(name="🖥️ Sistem", value=platform.system())
        embed.set_footer(text="Waifu-chan ❤️ aktif & setia di servermu")
        await ctx.send(embed=embed)

    @bot.command(name="waifuhelp")
    async def waifuhelp(ctx):
        embed = discord.Embed(
            title="📖 Daftar Perintah Waifu-chan",
            description="Gunakan prefix `~` saat memanggil command.\nCommand dibagi ke Umum & Admin.",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📌 Command Umum",
            value=(
                "`~ping` — Cek status bot\n"
                "`~waifuhelp` — Lihat daftar perintah\n"
                "`~botinfo` — Info bot & sistem\n"
                "`~peraturan` — Tampilkan semua peraturan\n"
                "`~cekvideo` — Cek video terbaru\n"
                "`~cekpost` — Cek post komunitas"
            ),
            inline=False
        )

        embed.add_field(
            name="🔧 Command Admin & Owner",
            value=(
                "`~forward #channel <pesan>` — Kirim embed admin\n"
                "`~to <pesan> #channel` — Kirim pesan anonim\n"
                "`~kickout @user` — Kick user dari server\n"
                "`~vkick @user` — Keluarkan dari voice\n"
                "`~tambahperaturan` / `~hapusperaturan` / `~editperaturan` — Kelola peraturan\n"
                "`~resetperaturan` / `~clear` / `~confirmclear` — Bersihkan peraturan\n"
                "`~setchannel` — Atur channel utama notifikasi\n"
                "`~cekpost_all` — Cek semua post komunitas"
            ),
            inline=False
        )

        embed.set_footer(text="Waifu-chan siap jadi teman komunitasmu ✨")
        await ctx.send(embed=embed)
