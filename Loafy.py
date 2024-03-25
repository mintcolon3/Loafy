import discord
import random
import asyncio
import emojis
import private
import specialbutter
from discord.ext import commands
from data import loadbutter, savebutter

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='^', intents=intents)

user_butter = loadbutter()

async def check_roles(guild):
    Jam_role = discord.utils.get(guild.roles, name="Jam'd")
    if not Jam_role:
        colour = discord.Colour(0xDE3163)
        perms = discord.Permissions(send_messages=False, send_messages_in_threads=False, add_reactions=False)
        Jam_role = await guild.create_role(name="Jam'd", colour=colour, permissions=perms)
    for channel in guild.text_channels:
        await channel.set_permissions(Jam_role, send_messages=False, send_messages_in_threads=False, add_reactions=False)

    purpl = discord.utils.get(guild.roles, name="purpl")
    if not purpl:
        colour = discord.Colour(0x9b59b6)
        await guild.create_role(name="purpl", colour=colour)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="butter"))

    print('slash commands syncing...')
    await bot.tree.sync()
    print('slash commands synced.\n')

    print('roles syncing...')
    for guild in bot.guilds:
        await check_roles(guild)
    print('roles synced.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('`This command does not exist.`')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('`You do not have the required permissions to run this command.`')

@bot.event
async def on_guild_join(guild):
    await check_roles(guild)

@bot.event
async def on_guild_channel_create(channel):
    Jam_role = discord.utils.get(channel.guild.roles, name="Jam'd")
    await channel.set_permissions(Jam_role, send_messages=False, send_messages_in_threads=False, add_reactions=False)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    content = message.content.lower()

    if content == '🧈':
        global user_butter
        user_id = str(message.author.id)
        user_butter.setdefault(user_id, [0, 0, 0])
        Jam_role = discord.utils.get(message.guild.roles, name="Jam'd")
        butter = random.choices([1, 2, 3], weights = [100, 10*(user_butter[user_id][2]+1), 5/(user_butter[user_id][2]+1)])
        if random.randint(1, 20) == 1:
            await message.author.add_roles(Jam_role)
            await message.add_reaction(emojis.jam)
            await message.reply('you got a jam. >:(')
            await asyncio.sleep(60)
            await message.author.remove_roles(Jam_role)
        elif butter == [3]:
            user_butter[user_id][2] += 1
            exotic_butter = random.choice(emojis.exotic_all)
            await message.add_reaction(exotic_butter)
            await message.reply(f'you got the exotic butter {exotic_butter}!\nyour exotic butter count is `{user_butter[user_id][2]}`.')
        elif butter == [2]:
            user_butter[user_id][1] += 1
            await message.add_reaction(emojis.butter2)
            await message.reply('you got the special butter!')
        elif butter == [1]:
            user_butter[user_id][0] += 1
            await message.add_reaction(emojis.butter)
        savebutter(user_butter)

    if 'butter' in content:
        if '^' not in content:
            replies = [
                'Holy shit! Is that a motherfucking 🧈 reference???',
                'Holy shit! Is that a motherfucking butter reference???',
                'https://media.discordapp.net/attachments/1217504702023991399/1217510803561910415/clickbait_butter.png?ex=66044a4b&is=65f1d54b&hm=a82863a6922f96f18ec039282d56f32ea357aa6e7edfe72a7339f09afa313c03&=&format=webp&quality=lossless&width=606&height=606',
                '🗣️🧈🧈🧈',
                'BUTTER IN THE HOLE!!!',
                'google butter'
            ]
            await message.reply(random.choice(replies))

    if content == "what's the bot deserving of the highest place on bread lb":
        await message.reply("The bot deserving of the highest place on bread lb is Loafy, the butter-loving bot.")
        if random.randint(1, 5) == 1:
            await message.reply(':0 loafy lore')

    await bot.process_commands(message)

@bot.hybrid_command(brief="get jam'd >:3", help="times you out for 1 minute")
async def jam(ctx):
    Jam_role = discord.utils.get(ctx.guild.roles, name="Jam'd")
    await ctx.author.add_roles(Jam_role)
    await ctx.reply(emojis.jam)
    await ctx.send('you got a jam. >:(')
    await asyncio.sleep(60)
    await ctx.author.remove_roles(Jam_role)

@bot.hybrid_command(brief="purpl role", help="1/20 chance of getting the 'purpl' role")
async def purpl(ctx):
    purpl = discord.utils.get(ctx.guild.roles, name="purpl")
    if random.randint(1, 20) == 1:
        await ctx.author.add_roles(purpl)
        await ctx.reply("`added role 'purpl'`")
    else:
        await ctx.defer(ephemeral=True)
        await ctx.reply('you didnt get the purpl role :(')

@bot.hybrid_group(invoke_without_command=True, brief="🧈")
async def butter(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.reply('🧈')

@butter.command(brief="view your butter stats")
async def stats(ctx, user: discord.User = commands.parameter(default=None, description="(optional)")):
    if user:
        user_id = str(user.id)
        title = f"butter stats for `{user.display_name}`"
    else:
        user_id = str(ctx.author.id)
        title = f"**butter stats for `{ctx.author.display_name}`**\n"
    if user_id in specialbutter.specialbutter.keys():
        butter = specialbutter.specialbutter[user_id]
    else:
        butter = user_butter.get(user_id, [0, 0, 0])
    
    description = f"{emojis.butter} - {butter[0]}\n"
    description += f"{emojis.butter2} - {butter[1]}\n"
    description += f"{emojis.exotic} - {butter[2]}\n\n"
    description += f"total butter - {butter[0] + butter[1] + butter[2]}"

    await ctx.reply(embed=discord.Embed(title=title, description=description, color=0x5865F2))

@butter.command(brief="check your chances of butters")
async def chance(ctx, user: discord.User = commands.parameter(default=None, description="(optional)")):
    if user:
        user_id = str(user.id)
        title = f"**butter chance for `{user.display_name}`**\n"
    else:
        user_id = str(ctx.author.id)
        title = f"**butter chance for `{ctx.author.display_name}`**\n"
    
    weights = [100, 10*(user_butter[user_id][2]+1), 5/(user_butter[user_id][2]+1)]
    description = f"{emojis.butter} - {round(((weights[0]/sum(weights))*100), 2):.2f}%\n"
    description += f"{emojis.butter2} - {round(((weights[1]/sum(weights))*100), 2):.2f}%\n"
    description += f"{emojis.exotic} - {round(((weights[2]/sum(weights))*100), 2):.2f}%"

    await ctx.reply(embed=discord.Embed(title=title, description=description, color=0x5865F2))

bot.run(private.TOKEN)