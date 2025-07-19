from discord.ext import commands
import discord

def setup_botinfo_commands(bot):

    @bot.command()
    async def ping(ctx):
        await ctx.send(f"Pong! 🏓 `{round(bot.latency * 1000)}ms`")

    @bot.command()
    async def waifuhelp(ctx):
        embed = discord.Embed(
            title="✨ Daftar Perintah Waifu-chan",
            description="Berikut semua command yang tersedia saat ini:",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="🧾 Manajemen Peraturan",
            value=(
                "`~peraturan` - Tampilkan daftar peraturan\n"
                "`~tambahperaturan` - Tambah peraturan baru (modal)\n"
                "`~editperaturan <no>` - Edit peraturan ke-n\n"
                "`~hapusperaturan <no>` - Hapus peraturan ke-n\n"
                "`~resetperaturan` - Reset semua peraturan\n"
                "`~cariaturan <kata>` - Cari peraturan berdasarkan kata kunci"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ Admin Utility",
            value=(
                "`~clear <jumlah>` [opsi: user, keyword] - Hapus pesan dengan filter & tombol konfirmasi\n"
                "`~tendangpengguna <user>` - Kick member\n"
                "`~to <channel_id> <pesan>` - Kirim pesan manual ke channel\n"
                "`~cekpost` / `~cekpost all` - Cek post komunitas terbaru\n"
                "`~cekvideo` - Cek video YouTube terbaru"
            ),
            inline=False
        )

        embed.add_field(
            name="🎀 Command Umum",
            value=(
                "`~ping` - Cek koneksi bot\n"
                "`~waifuhelp` - Daftar command Waifu-chan❤️"
            ),
            inline=False
        )

        embed.set_footer(text="Waifu-chan v1.0 • All systems online 💖")
        await ctx.send(embed=embed)