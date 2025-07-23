from discord.ext import commands
import discord

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
            title="📖 Bantuan Waifu-chan",
            description="Berikut adalah daftar command yang tersedia.\nGunakan prefix `~` untuk memanggil perintah.",
            color=discord.Color.purple()
        )

        # 📌 Umum
        embed.add_field(
            name="📌 Command Umum",
            value=(
                "`~ping` — Cek status bot\n"
                "`~waifuhelp` — Lihat daftar perintah\n"
                "`~botinfo` — Info bot dan daftar command aktif\n"
                "`~peraturan` — Tampilkan semua peraturan\n"
                "`~cekvideo` — Cek video terbaru Muse Indonesia\n"
                "`~cekpost` — Cek post komunitas terbaru"
            ),
            inline=False
        )

        # 🔧 Admin & Owner
        embed.add_field(
            name="🔧 Command Admin & Owner",
            value=(
                "`~forward #channel <pesan>` — Kirim embed admin ke channel tertentu\n"
                "`~to <pesan>` — Kirim pesan anonim ke channel aktif\n"
                "`~vkick @user` — Keluarkan user dari voice channel\n"
                "`~kickout @user` — Kick user dari server\n"
                "`~clear` / `~confirmclear` — Bersihkan semua peraturan\n"
                "`~tambahperaturan` / `~editperaturan` / `~hapusperaturan` — Kelola peraturan\n"
                "`~resetperaturan` — Reset seluruh daftar peraturan\n"
                "`~setchannel` — Atur channel utama notifikasi\n"
                "`~cekpost_all` — Cek semua post komunitas tanpa filter"
            ),
            inline=False
        )

        embed.set_footer(text="Waifu-chan siap jadi teman komunitasmu yang cerewet tapi berguna 💬💕")
        await ctx.send(embed=embed)
