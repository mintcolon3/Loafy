import discord
import random
import asyncio
import emojis
import private
from data import loadbutter, savebutter

user_butter = loadbutter()

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
    if not user or user == message.author:
        if time < 1:
            time = 1
        Jam_role = discord.utils.get(message.guild.roles, name="Jam'd")
        await message.author.add_roles(Jam_role)
        await message.add_reaction(emojis.jam)
        await message.reply('you got a jam. >:(')
        await asyncio.sleep(60*time)
        await message.author.remove_roles(Jam_role)
    else:
        if message.author.id == private.owner_id or message.author.get_role(private.anarchy_mod_id):
            if time < 0:
                time = 1
            Jam_role = discord.utils.get(message.guild.roles, name="Jam'd")
            await user.add_roles(Jam_role)
            await message.add_reaction(emojis.jam)
            await message.reply(f'{user.name} got a jam. >:(')
            await asyncio.sleep(60*time)
            await user.remove_roles(Jam_role)
        else:
            await message.reply('you need to be the owner to run this command.')