import discord
import random
import datetime
import os
import private
import json
import private_commands
from discord.ext import commands, tasks

async def printlog(self, input):
    channel = discord.utils.get(self.bot.get_all_channels(), id=1261742559668207636)
    print(input)
    await channel.send(f"```{input}```")

def load():
    file = open('chloe\kirbo.json')
    filedata = json.load(file)
    return filedata

def save(data):
    with open('chloe\kirbo.json', 'w') as file:
        json.dump(data, file, indent=4)

user_kirbo = load()
time = datetime.time(hour=23, minute=00, tzinfo=datetime.timezone.utc)

async def daily(self, reason):
    global user_kirbo
    for key, value in user_kirbo.items():
        user_kirbo[key][1] += 10 + user_kirbo[key][2]
        if user_kirbo[key][1] > 7 * (10 + user_kirbo[key][2]):
            user_kirbo[key][1] = 7 * (10 + user_kirbo[key][2])
    save(user_kirbo)
    await printlog(self, input=f"\nstored kirbo rolls have increased\nreason: {reason}\n")
    channel = discord.utils.get(self.bot.get_all_channels(), id=1254482628917203127)
    achannel = discord.utils.get(self.bot.get_all_channels(), id=1254105197547094128)
    await channel.send("<@&1323571811266461716>\nDaily rolls have been reset.")


class chloe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_refresh.start()

    # ----------------------------------------------
    # ----------------- KIRBO GAME -----------------
    # ----------------------------------------------
    
    def cog_unload(self):
        self.daily_refresh.cancel()
    
    @tasks.loop(time=time)
    async def daily_refresh(self):
        await daily(self, reason="daily rolls")
        for channel_id in private.krefresh:
            channel = discord.utils.get(self.bot.get_all_channels(), id=channel_id)

            reply = "Daily rolls have been reset."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            
            await channel.send(embed=reply_embed)
    
    @commands.group(name="c!kirbo", brief="kirbo", aliases=["kirbo", "killbot"])
    async def kirbo(self, ctx):
        await private.cprefix(ctx)

    @kirbo.command(brief="kirbo")
    async def roll(self, ctx, loop: int = 1):
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, [0, 20, 0, 0, 0])

        if loop <= 0:
            reply = "# <:thinkies_cat:1254100324751249521>"
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            
            await ctx.reply(embed=reply_embed)
            os._exit()

        if user_kirbo[user_id][1] - loop < 0:
            reply = "That exceeds the amount of daily rolls you have."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            
            await ctx.reply(embed=reply_embed)
            os._exit()

        c = user_kirbo[user_id][3] + 1
        dc = (user_kirbo[user_id][3]*1.5) + 1
        gc = (user_kirbo[user_id][3]*2) + 1
        kirbos = [1, 3, 5, 8, 10, 12, 14, 16, 25, 35, 50, 70, 100, 500]
        replies = [
            '<:kirbo:1314946641836511355>', '<:kirbo_green:1314946640410574899>', '<:kirbo_pink:1314946638749634563>',
            '<:Easy:1314949853838577725>', '<:Normal:1314949896150716447>', '<:Hard:1314949924412194816>',
            '<:Harder:1314949962576039978>', '<:Insane:1314950004309491773>', '<:EasyDemon:1314950046445342800>',
            '<:MediumDemon:1314950112132206684>', '<:HardDemon:1314950166415147069>', '<:InsaneDemon:1314950220634656918>',
            '<:ExtremeDemon:1314950243728621649>', '<:GrandpaDemon:1314950272887554069>'
        ]
        kirbo_roll = random.choices(population = kirbos, weights = [1900, 200*c, 60*c, 20*c, 18*c, 16*c, 14*c, 12*c, 6*dc, 5*dc, 4*dc, 2*dc, 1*dc, 0.1*gc], k=loop)
        fullreply = "# "
        count = 0
        totalkirbo = 0
        for value in kirbo_roll:
            reply = replies[kirbos.index(kirbo_roll[count])]
            fullreply += f"{reply}"
            totalkirbo += kirbo_roll[count]
            count += 1
        reply_embed = discord.Embed(description=fullreply, color=0xffd057)
        
        await ctx.reply(embed=reply_embed)
        user_kirbo[user_id][0] += totalkirbo
        user_kirbo[user_id][1] += -loop
        user_kirbo[user_id][4] += totalkirbo
        save(user_kirbo)
        
    @kirbo.command(brief="kirbo")
    async def stats(self, ctx, user: discord.User = commands.parameter(default=None, description="(optional)")):
        reply_embed = discord.Embed(color=0xffd057)
        
        if not user:
            user = ctx.author
        kirbo = user_kirbo.get(str(user.id), [0, 20, 0, 0])
        username = user.display_name

        reply = f"""
            {username} has **{kirbo[0]}** kirbos.
            {username} has **{kirbo[3]}** kirbo converters.
            {username} has **{kirbo[2] + 10}** daily rolls. (**{kirbo[2]}** extra daily rolls)

            
            {username} can roll **{kirbo[1]}** more times today."""
        
        reply_embed.add_field(name=f"stats for {username}:", value=reply)
        await ctx.reply(embed=reply_embed)

    @kirbo.command(brief="kirbo", help="run c!kirbo shop to view items.", aliases=["market"])
    async def shop(self, ctx):
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, [0, 20, 0, 0])
        reply = f"""
        Welcome to the Kirbo Market.
        You have **{user_kirbo[user_id][0]}** kirbos to spend.
        Buy items with `c!kirbo buy <amount> <item>`.

        **Extra daily roll (*alias: roll*)** - 50 kirbos ({user_kirbo[user_id][2]})
        Increases the amount of rolls you can make  every day by 1.
        
        **Kirbo converter (*alias: converter*)** - {int(150*(1.5**user_kirbo[user_id][3]))} kirbos ({user_kirbo[user_id][3]}/25)
        Increases your chance of rolling a better kirbo."""
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        
        await ctx.reply(embed=reply_embed)
        os._exit()

    @kirbo.command(brief="kirbo")
    async def buy(self, ctx, amount: int, *, item: str):
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, [0, 20, 0, 0])
        shop = {
            "extra daily roll" : [50, 2, "extra daily rolls"],
            "roll" : [50, 2, "extra daily rolls"],
            "kirbo converter" : [int(150*(1.5**user_kirbo[user_id][3])), 3, "kirbo converters"],
            "converter" : [int(150*(1.5**user_kirbo[user_id][3])), 3, "kirbo converters"],
        }

        amount = 1 if amount < 1 else amount

        if item == "kirbo converter" or item == "converter":
            if user_kirbo[user_id][3] >= 25:
                reply = "You have max kirbo converters."
                reply_embed = discord.Embed(description=reply, color=0xffd057)
                
                await ctx.reply(embed=reply_embed)

                os._exit("nya")
            
            amount = 1

        if shop[item][0] * amount > user_kirbo[user_id][0]:
            reply = "Looks like you don't have enough kirbos to buy that."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            
            await ctx.reply(embed=reply_embed)
            os._exit()

        user_kirbo[user_id][0] += -(shop[item][0] * amount)
        user_kirbo[user_id][shop[item][1]] += amount
        reply = f"You have bought {amount} {shop[item][2]}. You now have {user_kirbo[user_id][shop[item][1]]} of them.\nYou have **{user_kirbo[user_id][0]}** kirbos remaining."
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        
        await ctx.reply(embed=reply_embed)

        if item == "extra daily roll":
            user_kirbo[user_id][1] += amount

        save(user_kirbo)

    @kirbo.command(name="leaderboard", aliases=["lb"], brief="kirbo")
    async def leaderboard(self, ctx, name: str = "lifetime"):
        if await private_commands.extra_lb(self.bot, ctx, name) == True: return
        name = name.lower()

        leaderboards = {
            "lifetime" : [4, "lifetime kirbos"],
            "kirbo" : [0, "kirbos"],
            "roll" : [2, "maximum daily rolls"],
            "converter" : [3, "kirbo converters"]
        }

        if name not in leaderboards:
            reply = """**Leaderboards**
                lifetime: lifetime kirbos
                kirbo: kirbos
                roll: maximum daily rolls
                converter: kirbo converters"""
            reply_embed = discord.Embed(color=0xffd057, description=reply)
            
            await ctx.reply(embed=reply_embed)
            os.exit()

        sorted_data = sorted(user_kirbo.items(), key=lambda item: item[1][leaderboards[name][0]], reverse=True)
        top = sorted_data[:10]

        reply = "0.‎ **kirbo:** ∞\n"
        for x in top:
            user = ctx.guild.get_member(int(x[0]))
            reply += f"{top.index(x)+1}. **{user.display_name if user != None else x[0]}:** {x[1][leaderboards[name][0]] + 10 if name == 'roll' else x[1][leaderboards[name][0]]} \n"

        reply_embed = discord.Embed(color=0xffd057)
        
        reply_embed.add_field(name=f"**Leaderboard for {leaderboards[name][1]}**", value=reply)
        await ctx.reply(embed=reply_embed)
    
    @kirbo.command(brief="kirbo")
    async def rolls(self, ctx):
        kirbo = user_kirbo.get(str(ctx.author.id), [0, 20, 0, 0])
        reply_embed = discord.Embed(color=0xffd057)
        
        reply_embed.add_field(name="", value=f"You have **{kirbo[1]}** rolls remaining.")
        await ctx.reply(embed=reply_embed)


    @kirbo.command(hidden=True)
    async def reset(self, ctx, full: bool = False):
        await private.cowner(ctx)
        await daily(self, reason=f"reset by {ctx.author.name}")
        reply = "Daily rolls have been reset."
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        
        await ctx.reply(embed=reply_embed)