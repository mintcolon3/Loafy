import discord
import random
import emojis
import private
import specialbutter
import butter as butter_commands
from discord.ext import commands
from data import loadbutter

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
        await channel.set_permissions(Jam_role, send_messages=False, send_messages_in_threads=False, add_reactions=False, create_public_threads=False, create_private_threads=False)

    purpl = discord.utils.get(guild.roles, name="purpl")
    if not purpl:
        colour = discord.Colour(0x9b59b6)
        await guild.create_role(name="purpl", colour=colour)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="butter"))

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
            '<:butter_boop:1235867997353279499>'
        ]
        await message.reply(random.choice(replies))

    if content == "what's the bot deserving of the highest place on bread lb":
        await message.reply("The bot deserving of the highest place on bread lb is Loafy, the butter-loving bot.")
        if random.randint(1, 5) == 1:
            await message.channel.send(':0 loafy lore')

    await bot.process_commands(message)

@bot.command(brief="get jam'd >:3", help="times you out for 1 minute")
async def jam(ctx, user: discord.User = None, time: int = 1):
    await butter_commands.jam(ctx.message, user, time)

@bot.command(brief="purpl role", help="1/20 chance of getting the 'purpl' role")
async def purpl(ctx):
    purpl = discord.utils.get(ctx.guild.roles, name="purpl")
    if random.randint(1, 20) == 1:
        await ctx.author.add_roles(purpl)
        await ctx.reply("`added role 'purpl'`")
    else:
        await ctx.reply('you didnt get the purpl role :(')

@bot.group(invoke_without_command=True, brief="🧈")
async def butter(ctx):
    if ctx.invoked_subcommand is None:
        await butter_commands.butter(ctx.message)

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