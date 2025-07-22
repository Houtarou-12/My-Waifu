from discord.ext import commands
from discord import ui, ButtonStyle
import discord
import asyncio
from discord import TextStyle
import os
FORWARD_CHANNEL_ID = int(os.getenv("FORWARD_CHANNEL_ID", "0"))

def setup_admin_owner_commands(bot, COMMUNITY_CHANNEL_ID, VIDEO_CHANNEL_ID, YT_CHANNEL_URL, sent_post_ids):

    # 🧹 Clear dengan tombol & validasi target
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def clear(ctx, jumlah: int = 15, user: discord.Member = None, *, keyword: str = None):
        if jumlah < 1 or jumlah > 100:
            await ctx.send("❌ Jumlah harus antara 1–100.")
            return

        class ConfirmClearView(ui.View):
            def __init__(self):
                super().__init__(timeout=20)

            @ui.button(label="🟥 Hapus", style=ButtonStyle.danger)
            async def confirm(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("❌ Kamu tidak memicu command ini.", ephemeral=True)
                    return

                def check(m):
                    if user and m.author.id != user.id:
                        return False
                    if keyword and keyword.lower() not in m.content.lower():
                        return False
                    return True

                # Purge dengan limit ekstra agar pesan target tetap dihitung akurat
                deleted = await ctx.channel.purge(limit=jumlah + 2, check=check)

                # Pesan konfirmasi → kirim lalu hapus manual, agar tidak dihitung
                msg = await interaction.channel.send(
                    f"🧹 `{ctx.author.display_name}` menghapus {len(deleted)} pesan.",
                    delete_after=5
                )
                await asyncio.sleep(1)
                await msg.delete()
                self.stop()

            @ui.button(label="❌ Batal", style=ButtonStyle.secondary)
            async def cancel(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("❌ Kamu tidak memicu command ini.", ephemeral=True)
                    return
                await interaction.response.send_message("⚠️ Penghapusan dibatalkan.", ephemeral=True)
                self.stop()

        msg_text = f"⚠️ Kamu akan menghapus {jumlah} pesan"
        if user:
            msg_text += f" dari `{user.display_name}`"
        if keyword:
            msg_text += f" yang mengandung kata: `{keyword}`"
        await ctx.send(msg_text, view=ConfirmClearView())

    @bot.command(name="forward")
    @commands.has_permissions(administrator=True)
    async def forward(ctx, *, isi: str = None):
        if not isi or isi.strip() == "":
            await ctx.send("❌ Format: `~forward <isi pesan>`")
            return

        embed = discord.Embed(
            title="📢 Pesan dari Admin",
            description=isi.strip(),
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Disampaikan oleh {ctx.author.display_name}")

        class BalasanModal(ui.Modal, title="Kirim Balasan"):
            respon = ui.TextInput(label="Isi Balasan", style=TextStyle.paragraph, required=True)
 
            async def on_submit(self, interaction: discord.Interaction):
                embed_reply = discord.Embed(
                    title="✉️ Balasan untuk Admin",
                    description=self.respon.value,
                    color=discord.Color.green()
                )
                embed_reply.set_footer(text=f"Dikirim oleh {interaction.user.display_name}")
                await interaction.response.send_message(embed=embed_reply, ephemeral=True)

        class ForwardView(ui.View):
            @ui.button(label="✉️ Balas", style=ButtonStyle.primary)
            async def balas(self, interaction: discord.Interaction, button: ui.Button):
                await interaction.response.send_modal(BalasanModal())

            @ui.button(label="👍 Setuju", style=ButtonStyle.success)
            async def setuju(self, interaction: discord.Interaction, button: ui.Button):
                await interaction.response.send_message("✅ Terima kasih atas responmu!", ephemeral=True)

            @ui.button(label="❌ Tidak Setuju", style=ButtonStyle.danger)
            async def tidak_setuju(self, interaction: discord.Interaction, button: ui.Button):
                await interaction.response.send_message("⚠️ Opini kamu sudah dicatat!", ephemeral=True)

        target_channel = target_channel = bot.get_channel(FORWARD_CHANNEL_ID)
        if target_channel and target_channel != ctx.channel:
            await target_channel.send(embed=embed, view=ForwardView())
            await ctx.send(f"✅ Pesan berhasil diteruskan ke <#{FORWARD_CHANNEL_ID}>.")
        else:
            await ctx.send(embed=embed, view=ForwardView())
