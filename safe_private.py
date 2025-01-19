import discord
import os
import praw

TOKEN = ""
TEST_TOKEN = ""
EMOJI_TOKEN = ""
owner_id = 1170381506460536905
anarchy_mod_id = 958512048306815056

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="HIG-bot by u/blahajttttx",
)

krefresh = [1259121671017594882]

async def cowner(ctx):
    if ctx.author.id not in [1170381506460536905, 979758746760777798]:
        reply = "You cannot run this command."
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        reply_embed.set_author(name="Chloe's bot", icon_url="https://cdn.discordapp.com/avatars/1258789111414788137/18a9318b181469541f2494c12d59bec8.webp?")
        await ctx.reply(embed=reply_embed)

        os._exit(1)

async def lowner(ctx):
    if ctx.author.id != owner_id:
        await ctx.reply("you cannot run this command.")
        os._exit(1)

async def cprefix(ctx):
    if ctx.prefix == '^':
        os._exit(1)

async def lprefix(ctx):
    if ctx.prefix == 'c!':
        os._exit(1)

async def pchannel(ctx):
    if ctx.channel.id != 1259121671017594882:
        os._exit(1)

async def npchannel(ctx):
    if ctx.channel.id == 1259121671017594882:
        return