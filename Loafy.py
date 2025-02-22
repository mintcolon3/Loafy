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
counting = {}

async def check_roles(guild):
    purpl = discord.utils.get(guild.roles, name="purpl")
    if not purpl:
        colour = discord.Colour(0x9b59b6)
        await guild.create_role(name="purpl", colour=colour)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\n')
    await bot.change_presence(activity=discord.CustomActivity(name="im eepy :3"), status=discord.Status.online)

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

    if not message.guild:
        minty = await bot.fetch_user(private.owner_id)
        await minty.send(f"dm from {message.author}:\n{message.content}")
    
    if message.content.startswith('!^ ') and message.author.id == private.owner_id:
        await message.delete()
        
        if " -ds " in message.content:
            split = message.content.split(" -ds ")
            user = await bot.fetch_user(int(split[1]))
            await user.send(split[0].replace('!^ ', ''))
        elif message.reference: 
            reply_to = await message.channel.fetch_message(message.reference.message_id)
            if message.content.endswith(' -d'): await reply_to.author.send(message.content.replace('!^ ', '').replace(' -d', ''))
            else: await reply_to.reply(message.content.replace('!^ ', ''))
        else: await message.channel.send(message.content.replace('!^ ', ''))

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
            '@melodie remove jam from grambling',
            'butter butter go r/buttr',
            "Sorry, butter is not available right now\nA law banning butter has been enacted in the U.S. Unfortunately, that means you can't use butter right now.\nWe are fortunate that minty has indicated that she will work with us for a solution to reinstate butter once she takes office. Please stay tuned!"
        ]
        await message.reply(random.choice(replies))

    if content == "what's the bot deserving of the highest place on bread lb":
        await message.reply("The bot deserving of the highest place on bread lb is Loafy, the butter-loving bot.")
        if random.randint(1, 5) == 1:
            await message.channel.send(':0 loafy lore')
    
    if message.channel.id == 1216797203557781514 and random.randint(1, 10) == 1:
        await message.add_reaction("<:meow_boop:1264461237597638758>")

    if message.content.startswith(":") and not message.content.endswith(":"):
        global counting
        correct = 0
        int_values = "1234567890".split()

        for v in message.content.split()[1:]: correct += 1 if v not in int_values else 0

        if correct == 0:
            if int(message.channel.id) in counting.keys() and counting[message.channel.id][0] != 0 and counting[message.channel.id][1] != message.author.id:
                if int(message.content[1:]) == counting[message.channel.id][0]+1:
                    await message.add_reaction("✅")
                    counting[message.channel.id] = [int(message.content[1:]), message.author.id]
                else:
                    await butter_commands.jam(message, message.author, 1)
                    counting[message.channel.id] = [0, 0]
            elif int(message.channel.id) not in counting.keys() or counting[message.channel.id][0] == 0:
                if int(message.content[1:]) in [1, 3]:
                    await message.add_reaction("✅")
                    counting[message.channel.id] = [int(message.content[1:]), message.author.id]


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
    await ctx.reply(random.choices(population=["Mint is eepy", "Mint is eepy\nBut clo clo eepy tooooo", "The eepy fact of the day is the official creation of the eepy clan", "Evil Mint isnt eepy <:shock:1269669317381722114>"], weights=[12, 7, 2, 1])[0])

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx):
    await bot.add_cog(butter_commands.buttr(bot=bot))
    await bot.add_cog(chloe_commands.chloe(bot=bot))
    await ctx.reply("cogs loaded.")

@bot.command()
@commands.has_permissions(administrator=True)
async def count(ctx, arg, id: int = 0):
    global counting
    if arg == "dump":
        channel = discord.utils.get(bot.get_all_channels(), id=1261742559668207636)
        print(counting)
        await channel.send(f"```{counting}```")
    elif arg == "load":
        message = await ctx.fetch_message(id)
        counting = eval(message.content.replace("```", ""))

bot.run(private.TOKEN)