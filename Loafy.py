import discord
import praw
import random
import emojis
import os
import private
import special
import butter as butter_commands
import chloe.chloebot as chloe_commands
from discord.ext import commands, tasks
from data import loadbutter

reddit = private.reddit

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=('^', 'c!'), intents=intents)

user_butter = loadbutter()

async def check_roles(guild):
    purpl = discord.utils.get(guild.roles, name="purpl")
    if not purpl:
        colour = discord.Colour(0x9b59b6)
        await guild.create_role(name="purpl", colour=colour)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="eepyness"), status=discord.Status.idle)

    for guild in bot.guilds:
        bot.tree.clear_commands(guild=guild, type=discord.AppCommandType.chat_input)
    
    print('roles syncing...')
    for guild in bot.guilds:
        await check_roles(guild)
    print('roles synced.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('`You do not have the required permissions to run this command.`')

@bot.event
async def on_guild_join(guild):
    await check_roles(guild)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    content = message.content.lower()
    
    if message.content.startswith('!^ ') and message.author.id == private.owner_id:
        await message.delete()
        await message.channel.send(message.content.replace('!^ ', ''))

    if content == '🧈':
        await butter_commands.butter(message)

    if 'butter' in content and '^' not in content:
        replies = [
            'Holy shit! Is that a motherfucking 🧈 reference???',
            'Holy shit! Is that a motherfucking butter reference???',
            'https://media.discordapp.net/attachments/1217504702023991399/1217510803561910415/clickbait_butter.png?ex=66044a4b&is=65f1d54b&hm=a82863a6922f96f18ec039282d56f32ea357aa6e7edfe72a7339f09afa313c03&=&format=webp&quality=lossless&width=606&height=606',
            '🗣️🧈🧈🧈',
            'BUTTER IN THE HOLE!!!',
            'google butter',
            'https://media.discordapp.net/attachments/1223610285961777193/1235861835039768607/gd_butter.png?ex=6635e986&is=66349806&hm=e305c16c9a845d683fb4f48a03da0141ad11cdf50ea7a9f81529f339b385bf1d&=&format=webp&quality=lossless&width=1067&height=600',
            'oi butter',
            '<:butter_thinkies:1235864286182510643>',
            'buttercorrect oops',
            '<:butter_boop:1235867997353279499>',
            'eepy fact: buttr is eepy',
            '# EVIL BUTTER EVIL BUTTER EVIL BUTTER',
            '*steals your butter* >:3',
            'geobuttr',
            'woah its butter',
            'PUT DOWN YOUR JAM',
            'butter 2.2 when?',
            'youre a buttrkisser.',
            'butter <3',
            'feed some butter to your blahaj.',
            'hi hungry, im butter',
            'hi butter, im hungry',
            'SKITRON IS GOING TO BUTTER',
            'im feeling buttrlagged',
            '@ph03n1x :buttr:',
            '@melodie remove jam from grambling'
        ]
        await message.reply(random.choice(replies))

    if content == "what's the bot deserving of the highest place on bread lb":
        await message.reply("The bot deserving of the highest place on bread lb is Loafy, the butter-loving bot.")
        if random.randint(1, 5) == 1:
            await message.channel.send(':0 loafy lore')

    await bot.process_commands(message)

@bot.command(brief="purpl role", help="1/20 chance of getting the 'purpl' role")
async def purpl(ctx):
    await private.lprefix(ctx)
    purpl = discord.utils.get(ctx.guild.roles, name="purpl")
    if random.randint(1, 5) == 1:
        await ctx.author.add_roles(purpl)
        await ctx.reply("`added role 'purpl'`")
    else:
        await ctx.reply('you didnt get the purpl role :(')

@bot.command()
async def windy(ctx):
    await private.lprefix(ctx)
    subreddit = reddit.subreddit('egg_irl')
    top_post = next(subreddit.top('week', limit=1))
    
    title = top_post.title
    url = top_post.shortlink
    
    await ctx.send(f"# windy post of the week\n**{title}**\n{url}")

@bot.command(hidden=True)
async def eepy_fact(ctx):
    await private.lprefix(ctx)
    await ctx.reply(random.choices(population=["Mint is eepy", "Mint is eepy\nBut clo clo eepy tooooo", "Evil Mint isnt eepy <:shock:1269669317381722114>"], weights=[12, 7, 1])[0])

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx):
    await bot.add_cog(butter_commands.buttr(bot=bot))
    await bot.add_cog(chloe_commands.chloe(bot=bot))
    await ctx.reply("cogs loaded.")

bot.run(private.TOKEN)