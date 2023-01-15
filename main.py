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
    memo = await interaction.guild.create_text_channel(f"{interaction.user.name}のメモ", category=interaction.channel.category)
    await interaction.response.send_message(f"<@{interaction.user.id}>\n<#{memo.id}>にメモチャンネルを作成しました。", ephemeral=True)
    await memo.set_permissions(interaction.guild.default_role, view_channel=False)
    await memo.set_permissions(interaction.user, view_channel=True, send_messages=True)


@tree.command(name="delete")
async def memo(interaction: discord.Interaction):
    """メモチャンネルを削除します。"""
    await interaction.response.send_message("チャンネルを削除します。", ephemeral=True)
    channel = interaction.channel
    await channel.delete()

@tree.command(name="button")
async def button(interaction: discord.Interaction):
    """メモチャンネルを作るボタンを設置します。"""
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="作成", style=discord.ButtonStyle.primary)

    async def button_callback(interaction):
        for channel in client.get_all_channels():
            if channel == f"{interaction.user.name}のメモ":
                await interaction.response.send_message(f"メモチャンネルを複数作成することはできません。",ephemeral=True)
            else:
                memo = await interaction.guild.create_text_channel(f"{interaction.user.name}のメモ", category=interaction.channel.category)
                await interaction.response.send_message(f"<@{interaction.user.id}>\n<#{memo.id}>にメモチャンネルを作成しました。", ephemeral=True)
                await memo.set_permissions(interaction.guild.default_role, view_channel=False)
                await memo.set_permissions(interaction.user, view_channel=True, send_messages=True)

    button.callback = button_callback
    embed = discord.Embed(title="メモチャンネルの作成", description="あなた専用のあなた以外見ることのできないメモチャンネルを作ります。\n(Discordの仕様上、管理者には見えます)", color=0x00ff00)
    view.add_item(item=button)
    await interaction.response.send_message(embed=embed, view=view)

client.run(Token)