from discord.ext import commands
import discord
import platform

def setup_general_commands(bot):
    @bot.command(name="to")
    @commands.has_permissions(administrator=True)
    async def to(ctx, *, pesan: str = None):
        if not pesan:
            await ctx.send("❌ Format: `~to <pesan>`")
            return
        embed = discord.Embed(title="📩 Pesan Anonim", description=pesan.strip(), color=discord.Color.blurple())
        embed.set_footer(text="Dikirim oleh Waifu-chan (anonim)")
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
    @bot.command(name="kickout")
    @commands.has_permissions(kick_members=True)
    async def kickout(ctx, member: discord.Member = None, *, alasan: str = "Tidak ada alasan"):
        if not member:
            await ctx.send("❌ Format: `~kickout @user [alasan]`")
            return

        try:
            await member.kick(reason=alasan)
            await ctx.send(f"👢 {member.display_name} telah dikeluarkan dari server. Alasan: {alasan}")
        except Exception as e:
            await ctx.send(f"⚠️ Gagal kick: {e}")

    @bot.command(name="vkick")
    @commands.has_permissions(move_members=True)
    async def vkick(ctx, member: discord.Member = None):
        if not member or not member.voice:
            await ctx.send("❌ User tidak sedang berada di voice channel.")
            return

        try:
            await member.move_to(None)
            await ctx.send(f"🔊 {member.display_name} telah dikeluarkan dari voice channel.")
        except Exception as e:
            await ctx.send(f"⚠️ Gagal mengeluarkan: {e}")
