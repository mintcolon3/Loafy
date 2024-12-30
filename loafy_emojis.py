import discord
import private
import random as rand
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRole):
        await ctx.reply("You do not have the required permissions to run this command.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="minty cry"))
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print('slash commands synced.\n')

@bot.event
async def on_message(message):
    await message.reply("<:meow_boop:1264461237597638758>") if "<@&1262512214691287101>" in message.content and rand.randint(1, 3) == 1 else None
    await bot.process_commands(message)

@bot.hybrid_group(name="admin")
async def admin(ctx):
    return

@admin.command(name="send")
@commands.has_role("admin")
async def send(ctx, *, text):
    await ctx.channel.send(content=text)
    await ctx.reply("Message sent.", ephemeral=True)

@admin.command(name="edit")
@commands.has_role("admin")
async def edit(ctx, id, *, text):
    channel = ctx.channel
    msg = await channel.fetch_message(int(id))
    await msg.edit(content=text)
    await ctx.reply("Message edited.", ephemeral=True)

@bot.hybrid_command(name="emoji")
async def emoji(ctx, emoji):
    id = emoji.split(":")[2].replace(">", "")
    if emoji.startswith("a"):
        ext = "gif"
    else:
        ext ="png"
    await ctx.reply(f"https://cdn.discordapp.com/emojis/{id}.{ext}")

@bot.hybrid_command(name="random")
async def random(ctx):
    emojis = []
    for guild in bot.guilds:
        emojis.extend(guild.emojis)
    await ctx.reply(rand.choice(emojis))


bot.run(private.EMOJI_TOKEN)