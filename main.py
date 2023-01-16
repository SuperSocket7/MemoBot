import discord
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv('Token')
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()


@tree.command(name="memo")
async def memo(interaction: discord.Interaction):
    """メモチャンネルを作成します。"""
    memo_channel = await interaction.guild.create_text_channel(f"{interaction.user.name}のメモ",
                                                               category=interaction.channel.category)
    await interaction.response.send_message(
        f"<@{interaction.user.id}>\n<#{memo_channel.id}>にメモチャンネルを作成しました。", ephemeral=True)
    await memo_channel.set_permissions(interaction.guild.default_role, view_channel=False)
    await memo_channel.set_permissions(interaction.user, view_channel=True, send_messages=True)


@tree.command(name="delete")
async def delete(interaction: discord.Interaction):
    """メモチャンネルを削除します。"""
    if "のメモ" in interaction.channel.name:
        await interaction.response.send_message("チャンネルを削除します。", ephemeral=True)
        channel = interaction.channel
        await channel.delete()
    else:
        await interaction.response.send_message("メモチャンネル以外は削除できません。", ephemeral=True)


@tree.command(name="add")
async def add(interaction: discord.Interaction, user: discord.Member):
    """閲覧できる人を追加します。"""
    if "のメモ" in interaction.channel.name:
        channel = interaction.channel
        await channel.set_permissions(user, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"<@{user.id}>が閲覧できるようになりました。", ephemeral=True)
    else:
        await interaction.response.send_message("メモチャンネル以外は編集できません。", ephemeral=True)


@tree.command(name="button")
async def button(interaction: discord.Interaction):
    """メモチャンネルを作るボタンを設置します。"""
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="作成", style=discord.ButtonStyle.primary)

    async def button_callback(interaction):
        memo_channel = await interaction.guild.create_text_channel(f"{interaction.user.name}のメモ",
                                                                   category=interaction.channel.category)
        await interaction.response.send_message(
            f"<@{interaction.user.id}>\n<#{memo_channel.id}>にメモチャンネルを作成しました。", ephemeral=True)
        await memo_channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await memo_channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

    button.callback = button_callback
    embed = discord.Embed(title="メモチャンネルの作成",
                          description="あなた専用のあなた以外見ることのできないメモチャンネルを作ります。\n(Discordの仕様上、管理者には見えます)",
                          color=0x00ff00)
    view.add_item(item=button)
    await interaction.response.send_message(embed=embed, view=view)


client.run(Token)