from discord.ext import commands
import discord

def setup_botinfo_commands(bot):

    @bot.command()
    async def ping(ctx):
        await ctx.send(f"Pong! 🏓 `{round(bot.latency * 1000)}ms`")

    #Menggunakan Semua Command Waifu-chan❤️
    @bot.command(name="waifuhelp")
    async def waifuhelp(ctx):
        embed = discord.Embed(
            title="📖 Bantuan Waifu-chan",
            description="Gunakan prefix `~` untuk memanggil command.",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📺 Video & Komunitas",
            value=(
                "**~cekvideo** – Cek video terbaru Muse Indonesia dari RSS\n"
                "**~cekpost** – Cek post komunitas terbaru\n"
                "🔁 Otomatis notifikasi setiap 30–60 detik"
            ),
            inline=False
        )

        embed.add_field(
            name="✉️ Admin Tools",
            value=(
                "**~forward #channel <pesan>** – Kirim embed admin ke channel tertentu\n"
                "┗ Tombol: ✉️ Balas, 👍 Setuju, ❌ Tidak Setuju\n"
                "┗ Modal interaktif + auto delete command"
            ),
            inline=False
        )

        embed.add_field(
            name="📜 Info Bot",
            value=(
                "**~peraturan** – Tampilkan peraturan server\n"
                "**~botinfo** – Info bot & daftar command aktif"
            ),
            inline=False
        )

        embed.set_footer(text="Waifu-chan siap bantu ✨")
        await ctx.send(embed=embed)

        # ✉️ Admin & Pesan
        embed.add_field(
            name="✉️ Admin Tools",
            value=(
                "**~forward #channel <pesan>** – Kirim embed resmi ke channel tertentu\n"
                "┗ Tombol: ✉️ Balas, 👍 Setuju, ❌ Tidak Setuju\n"
                "┗ Modal balasan & auto-delete pesan asli"
            ),
            inline=False
        )

        # 📜 Informasi & Peraturan
        embed.add_field(
            name="📜 Info Bot",
            value=(
                "**~botinfo** – Info versi, uptime, dan status Waifu-chan\n"
                "**~peraturan** – Tampilkan embed peraturan server"
            ),
            inline=False
        )

        embed.set_footer(text="Waifu-chan siap bantu dan menjaga keharmonisan server ✨")
        await ctx.send(embed=embed)

    @bot.command(name="botinfo")
    async def botinfo(ctx):
        embed = discord.Embed(
            title="🤖 Info Waifu-chan",
            description="Bot anime untuk notifikasi & interaksi server.",
            color=discord.Color.pink()
        )

        embed.add_field(name="🆔 Bot ID", value=str(bot.user.id), inline=True)
        embed.add_field(name="📛 Nama", value=bot.user.name, inline=True)
        embed.add_field(name="🧠 Command Aktif", value=str(len(bot.commands)), inline=True)

        command_list = "\n".join(f"• `{cmd.name}`" for cmd in bot.commands if not cmd.hidden)
        embed.add_field(name="📋 Daftar Command", value=command_list or "Belum ada command.", inline=False)

        embed.set_footer(text="Waifu-chan aktif & siap melayani ❤️")
        await ctx.send(embed=embed)
