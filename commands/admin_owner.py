from discord.ext import commands
from discord import ui, ButtonStyle
import discord
import asyncio

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