from discord.ext import commands
from discord import ui, ButtonStyle, TextStyle
import discord
import json
import os

RULES_FILE = "rules.json"  # ← Ganti dari data.json

def setup_peraturan_commands(bot):

    # 💾 ── Helper fungsi JSON ──
    def load_rules():
        if os.path.exists(RULES_FILE):
            try:
                with open(RULES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ERROR] Gagal load rules: {e}")
        return []

    def save_rules(rules):
        try:
            with open(RULES_FILE, "w", encoding="utf-8") as f:
                json.dump(rules, f, indent=2, ensure_ascii=False)
            print(f"[SAVE] Peraturan: {len(rules)} item disimpan.")
        except Exception as e:
            print(f"[ERROR] Gagal save rules: {e}")

    # 📋 ── Tampilkan peraturan dengan embed pagination ──
    @bot.command()
    @commands.has_role("Admin")
    async def peraturan(ctx):
        rules = load_rules()
        if not rules:
            await ctx.send("⚠️ Belum ada peraturan yang dibuat.")
            return

        class RuleView(ui.View):
            def __init__(self, pages):
                super().__init__(timeout=60)
                self.pages = pages
                self.index = 0

            @ui.button(label="⬅️", style=ButtonStyle.primary)
            async def back(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user != ctx.author:
                    return await interaction.response.send_message("❌ Kamu tidak memulai command ini.", ephemeral=True)
                self.index = (self.index - 1) % len(self.pages)
                await interaction.response.edit_message(embed=self.pages[self.index])

            @ui.button(label="➡️", style=ButtonStyle.primary)
            async def next(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user != ctx.author:
                    return await interaction.response.send_message("❌ Kamu tidak memulai command ini.", ephemeral=True)
                self.index = (self.index + 1) % len(self.pages)
                await interaction.response.edit_message(embed=self.pages[self.index])

        chunks = [rules[i:i+5] for i in range(0, len(rules), 5)]
        embeds = []
        for idx, group in enumerate(chunks):
            desc = "\n".join([f"{i + 1 + idx*5}. {r}" for i, r in enumerate(group)])
            embed = discord.Embed(title="📋 Peraturan Server", description=desc, color=discord.Color.orange())
            embed.set_footer(text=f"Halaman {idx+1} dari {len(chunks)}")
            embeds.append(embed)

        await ctx.send(embed=embeds[0], view=RuleView(embeds))

    # ➕ ── Tambah peraturan via tombol & modal ──
    @bot.command()
    @commands.has_role("Admin")
    async def tambahperaturan(ctx):
        class RuleModal(ui.Modal, title="Tambah Peraturan Baru"):
            isi = ui.TextInput(label="Isi Peraturan", style=TextStyle.paragraph, placeholder="Masukkan isi peraturan...", required=True)

            async def on_submit(self, interaction: discord.Interaction):
                rules = load_rules()
                rules.append(self.isi.value)
                save_rules(rules)
                await interaction.response.send_message(f"✅ Peraturan baru ditambahkan:\n📌 `{self.isi.value}`", ephemeral=True)

        class RuleButtonView(ui.View):
            @ui.button(label="➕ Tambah Peraturan", style=ButtonStyle.success)
            async def open_modal(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user == ctx.author:
                    await interaction.response.send_modal(RuleModal())
                else:
                    await interaction.response.send_message("❌ Kamu tidak memulai command ini.", ephemeral=True)

        await ctx.send("📥 Klik tombol di bawah untuk menambahkan peraturan.", view=RuleButtonView())

    # 🗑️ ── Reset semua peraturan ──
    @bot.command()
    @commands.has_role("Admin")
    async def resetperaturan(ctx):
        save_rules([])
        await ctx.send("⚠️ Semua peraturan telah direset.")

    # ❌ ── Hapus peraturan berdasarkan nomor ──
    @bot.command()
    @commands.has_role("Admin")
    async def hapusperaturan(ctx, nomor: int = None):
        rules = load_rules()
        if not rules:
            return await ctx.send("⚠️ Tidak ada peraturan untuk dihapus.")
        if nomor is None or nomor < 1 or nomor > len(rules):
            return await ctx.send(f"❌ Nomor harus antara 1 dan {len(rules)}.")

        hapus = rules.pop(nomor - 1)
        save_rules(rules)
        await ctx.send(f"🗑️ Peraturan ke-{nomor} dihapus:\n❌ `{hapus}`")

    # 📝 ── Edit isi peraturan berdasarkan nomor ──
    @bot.command()
    @commands.has_role("Admin")
    async def editperaturan(ctx, nomor: int = None):
        rules = load_rules()
        if not rules:
            return await ctx.send("⚠️ Tidak ada peraturan untuk diedit.")
        if nomor is None or nomor < 1 or nomor > len(rules):
            return await ctx.send(f"❌ Nomor harus antara 1 dan {len(rules)}.")

        class EditModal(ui.Modal, title=f"Edit Peraturan #{nomor}"):
            new_text = ui.TextInput(label="Peraturan Baru", style=TextStyle.paragraph, default=rules[nomor - 1])

            async def on_submit(self, interaction: discord.Interaction):
                rules[nomor - 1] = self.new_text.value
                save_rules(rules)
                await interaction.response.send_message(f"✏️ Peraturan #{nomor} telah diperbarui:\n📌 `{self.new_text.value}`", ephemeral=True)

        class EditView(ui.View):
            @ui.button(label="✏️ Edit Peraturan", style=ButtonStyle.secondary)
            async def open_edit(self, interaction: discord.Interaction, button: ui.Button):
                if interaction.user == ctx.author:
                    await interaction.response.send_modal(EditModal())
                else:
                    await interaction.response.send_message("❌ Kamu tidak memulai command ini.", ephemeral=True)

        await ctx.send(f"📝 Klik tombol di bawah untuk mengedit peraturan ke-{nomor}.", view=EditView())

    @bot.command()
    @commands.has_role("Admin")
    async def cariaturan(ctx, *, keyword: str = None):
        rules = load_rules()
        if not rules:
            return await ctx.send("⚠️ Tidak ada peraturan yang tersedia.")
        if not keyword:
            return await ctx.send("❌ Format: `~cariaturan <kata kunci>`")

        hasil = [f"{i+1}. {r}" for i, r in enumerate(rules) if keyword.lower() in r.lower()]
        if not hasil:
            return await ctx.send(f"🔍 Tidak ditemukan peraturan dengan kata: `{keyword}`")

        embed = discord.Embed(
            title=f"🔍 Hasil Pencarian: '{keyword}'",
            description="\n".join(hasil),
            color=discord.Color.green()
        )
        embed.set_footer(text=f"{len(hasil)} peraturan ditemukan.")
        await ctx.send(embed=embed)