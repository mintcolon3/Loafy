import discord
import random
import asyncio
import datetime
import emojis
import private
import special
from data import loadbutter, savebutter
from discord.ext import commands


user_butter = loadbutter()

class buttr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="get jam'd >:3", help="times you out for 1 minute")
    async def jam(self, ctx, user: discord.User = None, time: int = 1):
        await private.lprefix(ctx)
        await jam(ctx.message, user, time)

    @commands.group(invoke_without_command=True, brief="🧈")
    async def butter(self, ctx):
        await private.lprefix(ctx)
        if ctx.invoked_subcommand is None:
            await butter(ctx.message)

    @butter.command(brief="view your butter stats")
    async def stats(self, ctx, user: discord.User = commands.parameter(default=None, description="(optional)")):
        await private.lprefix(ctx)
        if user:
            user_id = str(user.id)
            title = f"butter stats for `{user.display_name}`"
        else:
            user_id = str(ctx.author.id)
            title = f"**butter stats for `{ctx.author.display_name}`**\n"
        if user_id in special.specialbutter.keys():
            butter = special.specialbutter[user_id]
        else:
            butter = user_butter.get(user_id, [0, 0, 0])
    
        description = f"{emojis.butter} - {butter[0]}\n"
        description += f"{emojis.butter2} - {butter[1]}\n"
        description += f"{emojis.exotic} - {butter[2]}\n\n"
        description += f"total butter - {butter[0] + butter[1] + butter[2]}"

        await ctx.reply(embed=discord.Embed(title=title, description=description, color=0x5865F2))

    @butter.command(brief="check your chances of butters")
    async def chance(self, ctx, user: discord.User = commands.parameter(default=None, description="(optional)")):
        await private.lprefix(ctx)
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


async def butter(message):
    global user_butter
    user_id = str(message.author.id)
    user_butter.setdefault(user_id, [0, 0, 0])
    butter = random.choices([1, 2, 3], weights = [100, 10*(user_butter[user_id][2]+1), 5/(user_butter[user_id][2]+1)])
    if random.randint(1, 20) == 1:
        await jam(message)
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

async def jam(message, user, time):
    if message.author.id == private.owner_id or message.author.get_role(private.anarchy_mod_id):
        user = message.guild.get_member(user.id)
        time = 1 if time < 1 else time
        timeout = datetime.timedelta(minutes=1*time)
        await user.timeout(timeout)
        await message.add_reaction(emojis.jam)
        await message.reply(f'{user.name} got a jam. >:(')
    else:
        user = message.author
        time = 1 if time < 1 else time
        timeout = datetime.timedelta(minutes=1*time)
        await user.timeout(timeout)
        await message.add_reaction(emojis.jam)
        await message.reply('you got a jam. >:(')