import discord
import random
import datetime
import os
import private
import json
import private_commands
import asyncio
import typing
from chloe.kirbo_roll import kirbo_roll
from discord.ext import commands, tasks
from private import kdefault as df

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
        print(key)
        user_kirbo[key][1] += 10 + user_kirbo[key][2]
        if user_kirbo[key][1] > 7 * (10 + user_kirbo[key][2]):
            user_kirbo[key][1] = 7 * (10 + user_kirbo[key][2])
        print(user_kirbo[key][1])
    save(user_kirbo)
    await printlog(self, input=f"\nstored kirbo rolls have increased\nreason: {reason}\n")
    channel = discord.utils.get(self.bot.get_all_channels(), id=1254482628917203127)
    achannel = discord.utils.get(self.bot.get_all_channels(), id=1254105197547094128)
    await channel.send("Daily rolls have been reset.")


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
        global user_kirbo # gets user kirbo data
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, df) # sets the default for if the user hasnt rolled before

        if loop <= 0: # checks if the requested rolls are 0 or less, exits if true
            reply = "<:thinkies_cat:1254100324751249521>"
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            await ctx.reply(embed=reply_embed)
            return

        if user_kirbo[user_id][1] - loop < 0: # checks if the requested rolls are more than the user can roll, exits if true
            reply = "That exceeds the amount of daily rolls you have."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            await ctx.reply(embed=reply_embed)
            return

        rolls = kirbo_roll(loop, user_kirbo[user_id]) # rolls kirbos
        user_kirbo[user_id] = rolls[0] # sets new user kirbo values
        await ctx.reply(embed=rolls[1]) # replies with embed

        save(user_kirbo) # saves the new user kirbo values
        
    @kirbo.command(brief="kirbo")
    async def stats(self, ctx, user: discord.User = commands.parameter(default=None, description="(optional)"), page: str = "all"):
        reply_embed = discord.Embed(color=0xffd057)
        if page.lower() not in ["all", "main", "items"]: page = "all"
        if user: user = ctx.guild.get_member(user.id)
        if not user: user = ctx.author
        kirbo = user_kirbo.get(str(user.id), df)
        username = user.display_name
        al2_role = discord.utils.get(ctx.guild.roles, id=1336377462656995509)
        al2_check = al2_role in user.roles

        def c(v):
            reply = ""
            reply += f", {kirbo[8][0][v]}s" if kirbo[8][0][v] > 0 else ""
            reply += f", {kirbo[8][1][v]}g" if kirbo[8][1][v] > 0 else ""
            reply += f", {kirbo[8][2][v]}pk" if kirbo[8][2][v] > 0 else ""
            return reply

        main_reply = f"""
            {username} has **{kirbo[0]}** kirbos.
            {f'{username} has **{kirbo[6][0]}** silver.' if al2_check else '..'}
            {f'{username} has **{kirbo[6][1]}** gold.' if al2_check else '..'}
            {f'{username} has **{kirbo[6][2]}** pure kirbo.' if al2_check else '..'}
            {username} has **{kirbo[3]}** kirbo converters.
            {username} has **{kirbo[2] + 10}** daily rolls. (**{kirbo[2]}** extra daily rolls)

            {f'{username} has increased the extra daily roll cap {kirbo[7][0]} times.' if al2_check else '..'}
            {f'{username} has upgraded item quality {kirbo[7][1]} times.' if al2_check else '..'}
            {f'{username} has researched clusters {kirbo[7][2]} times.' if al2_check else '..'}
            
            {username} has rolled **{kirbo[4]}** kirbos in total.

            {username} can roll **{kirbo[1]}** more times today.""".replace("\n            ..", "")
        items_reply1 = f"""
            **{kirbo[5][0]}{c(0)}** <:kirbo:1314946641836511355>
            **{kirbo[5][1]}{c(1)}** <:kirbo_green:1314946640410574899>
            **{kirbo[5][2]}{c(2)}** <:kirbo_pink:1314946638749634563>
            **{kirbo[5][3]}{c(3)}** <:Easy:1314949853838577725>
            **{kirbo[5][4]}{c(4)}** <:Normal:1314949896150716447>
            **{kirbo[5][5]}{c(5)}** <:Hard:1314949924412194816>
            **{kirbo[5][6]}{c(6)}** <:Harder:1314949962576039978>"""
        items_reply2 = f"""
            **{kirbo[5][7]}{c(7)}** <:Insane:1314950004309491773>
            **{kirbo[5][8]}{c(8)}** <:EasyDemon:1314950046445342800>
            **{kirbo[5][9]}{c(9)}** <:MediumDemon:1314950112132206684>
            **{kirbo[5][10]}{c(10)}** <:HardDemon:1314950166415147069>
            **{kirbo[5][11]}{c(11)}** <:InsaneDemon:1314950220634656918>
            **{kirbo[5][12]}{c(12)}** <:ExtremeDemon:1314950243728621649>
            **{kirbo[5][13]}{c(13)}** <:GrandpaDemon:1314950272887554069>"""
        
        if page.lower() in ["all", "main"]: reply_embed.add_field(name=f"stats for {username}:", value=main_reply)
        if page.lower() in ["all", "items"]:
            reply_embed.add_field(name="Items" if page.lower() == "all" else f"Items for {username}", value=items_reply1)
            reply_embed.add_field(name="‎", value=items_reply2)
        await ctx.reply(embed=reply_embed)

    @kirbo.command(brief="kirbo", help="run c!kirbo shop to view items.", aliases=["market"])
    async def shop(self, ctx):
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, df)

        al2_role = discord.utils.get(ctx.guild.roles, id=1336377462656995509)
        if user_kirbo[user_id][3] == 20 and al2_role not in ctx.author.roles:
            reply = f"""
            Welcome to the Kirbo Market.
            You have **{user_kirbo[user_id]["al1"][0]}** kirbos to spend.
            Buy items with `c!kirbo buy <amount> <item>`.

            **Extra daily roll (*alias: roll*)** - 50 kirbos ({user_kirbo[user_id]["al1"][2]})
            Increases the amount of rolls you can make  every day by 1.

            **???** - 5000 kirbos
            ?????????????????????????????"""
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            await ctx.reply(embed=reply_embed)
            return

        reply = f"""
        Welcome to the Kirbo Market.
        You have **{user_kirbo[user_id][0]}** kirbos to spend.
        Buy items with `c!kirbo buy <item>` or `c!kirbo buy <amount> <item>`.

        **Extra daily roll (*alias: roll*)** - 50 kirbos ({user_kirbo[user_id][2]}/50)
        Increases the amount of rolls you can make  every day by 1.
        
        **Kirbo converter (*alias: converter*)** - {int(150*(1.2**user_kirbo[user_id][3]))} kirbos ({user_kirbo[user_id][3]}/20)
        Increases your chance of rolling a better kirbo."""
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        await ctx.reply(embed=reply_embed)

    @kirbo.command(brief="kirbo")
    async def buy(self, ctx, amount: typing.Optional[int], *, item: str):
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, df)

        al2_role = discord.utils.get(ctx.guild.roles, id=1336377462656995509)
        if item == "???" and user_kirbo[user_id][3] == 20 and al2_role not in ctx.author.roles:
            if user_kirbo[user_id]["al1"][0] < 5000:
                await ctx.reply(f"You do not have enough kirbos to buy this item.")
                return

            printlog(self, f"{ctx.author.name} has upgraded to access level 2.")
            await ctx.author.send("Thanks for buying ????????????????? :3\n\ntry running `c!help hidden` in the kirbuttr channel.")

            await ctx.author.add_roles(al2_role)
            user_kirbo[user_id]["al1"][0] += -5000
            save(user_kirbo)
            return

        shop = {
            "extra daily roll" : [50, 2, "extra daily rolls"],
            "roll" : [50, 2, "extra daily rolls"],
            "kirbo converter" : [int(150*(1.2**user_kirbo[user_id][3])), 3, "kirbo converters"],
            "converter" : [int(150*(1.2**user_kirbo[user_id][3])), 3, "kirbo converters"],
        }

        if amount == None: amount = 1
        if amount < 1: amount = 1
        item = item.lower()

        if item == "kirbo converter" or item == "converter":
            if user_kirbo[user_id][3] >= 20:
                reply = "You have max kirbo converters."
                reply_embed = discord.Embed(description=reply, color=0xffd057)
                await ctx.reply(embed=reply_embed)
                return
            
            amount = 1
        
        if item in ["extra daily roll", "roll"] and user_kirbo[user_id][2] + amount > 50 + user_kirbo[user_id][6][0]*20:
            reply = "You have max daily rolls."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            await ctx.reply(embed=reply_embed)
            return

        if shop[item][0] * amount > user_kirbo[user_id][0]:
            reply = "Looks like you don't have enough kirbos to buy that."
            reply_embed = discord.Embed(description=reply, color=0xffd057)
            await ctx.reply(embed=reply_embed)
            return

        user_kirbo[user_id][0] += -(shop[item][0] * amount)
        user_kirbo[user_id][shop[item][1]] += amount
        reply = f"You have bought {amount} {shop[item][2]}. You now have {user_kirbo[user_id][shop[item][1]]} of them.\nYou have **{user_kirbo[user_id][0]}** kirbos remaining."
        reply_embed = discord.Embed(description=reply, color=0xffd057)
        
        await ctx.reply(embed=reply_embed)

        if item in ["extra daily roll", "roll"]: user_kirbo[user_id][1] += amount

        save(user_kirbo)

    @kirbo.command(name="leaderboard", aliases=["lb"], brief="kirbo",
                   help="Leaderboards:\nlifetime: lifetime kirbos\nkirbo: kirbos\nroll: maximum daily rolls\nconverter: kirbo converters")
    async def leaderboard(self, ctx, name: str = "lifetime"):
        if await private_commands.extra_lb(self.bot, ctx, name) == True: return
        name = name.lower()

        leaderboards = {
            "lifetime" : [4, "lifetime kirbos"],
            "kirbo" : [0, "kirbos"],
            "roll" : [2, "maximum daily rolls"],
            "converter" : [3, "kirbo converters"],
        }

        if name not in leaderboards:
            reply_embed = discord.Embed(color=0xffd057, description="run `c!help kirbo lb` for a list of leaderboards")
            await ctx.reply(embed=reply_embed)
            return

        sorted_data = sorted(
            user_kirbo.items(),
            key=lambda item: item[1][leaderboards[name][0]]*(-1))
        top = sorted_data[:10]

        reply = "0.‎ **kirbo:** ∞\n"
        for x in top:
            member = ctx.guild.get_member(int(x[0]))

            if member != None: member_name = member.display_name
            elif x[0] in private.known_users: member_name = private.known_users[x[0]]
            else: x[0]

            if name == "roll": value = str(x[1][leaderboards[name][0]]+10)
            else: value = str(x[1][leaderboards[name][0]])

            reply += f"{top.index(x)+1}. **{member_name}:** {value} \n"

        reply_embed = discord.Embed(color=0xffd057)
        reply_embed.add_field(name=f"**Leaderboard for {leaderboards[name][1]}**", value=reply)
        await ctx.reply(embed=reply_embed)
    
    @kirbo.command(brief="kirbo")
    async def rolls(self, ctx):
        kirbo = user_kirbo.get(str(ctx.author.id), df)
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
    
    @kirbo.command(hidden=True)
    async def uroll(self, ctx, user_id: str):
        await private.cowner(ctx)
        global user_kirbo
        user_id = str(ctx.author.id)
        user_kirbo.setdefault(user_id, df)

        rolls = kirbo_roll(user_kirbo[user_id][1], user_kirbo[user_id])
        user_kirbo[user_id] = rolls[0]
        await ctx.reply(embed=rolls[1])

        save(user_kirbo)
    



    # ----------------------------------------------
    # ------- HIDDEN KIRBO (ACCESS LEVEL 2) --------
    # ----------------------------------------------


    @commands.group(name="c!hidden", aliases=["hidden", "hkirbo", "hidden_kirbo"])
    @commands.has_role(1336377462656995509)
    async def hidden(self, ctx):
        await private.cprefix(ctx)
    
    @hidden.command(name="shop", brief="list of items available in the hidden market")
    async def hshop(self, ctx):
        global user_kirbo
        user_id = str(ctx.author.id)

        qual_upgrade_prices = ["300 kirbos", "200 silver", "200 gold"]
        qual_upgrade_features = ["silver", "gold", "ultra"]
        cluster_prices = [300, 600, 900, 1200, 1500, 1800, 2100, 2500]
        reply = f"""
        Welcome to the Hidden Kirbo Market.
        You have **{user_kirbo[user_id][0]}** kirbos to spend.
        Buy items with `c!hidden buy <item>`.
        
        **Daily roll cap increase (*alias: cap*)** - {200+100*user_kirbo[user_id][7][0]} kirbos ({user_kirbo[user_id][7][0]}/5)
        Increases the cap of how many extra daily rolls you can buy by 20.
        
        **Quality upgrade {user_kirbo[user_id][7][1]+1} (*alias: upgrade*)** - {qual_upgrade_prices[user_kirbo[user_id][7][1]]}
        Allows you to roll {qual_upgrade_features[user_kirbo[user_id][7][1]]} quality items.
        
        **Cluster research {user_kirbo[user_id][7][2]+1} (*alias: cluster*)** - {cluster_prices[user_kirbo[user_id][7][2]]} kirbos
        Allows you to roll multiple items in one roll."""

        reply_embed = discord.Embed(description=reply, color=0x725628)
        await ctx.reply(embed=reply_embed)
    
    @hidden.command(name="buy", brief="hidden market")
    async def hbuy(self, ctx, *, item: str):
        global user_kirbo
        user_id = str(ctx.author.id)
        item = item.lower()
        lower = None

        if item in ["daily roll cap increase", "roll cap increase", "daily roll cap", "roll cap", "daily cap", "cap"]:
            if user_kirbo[user_id][0] < 200+100*user_kirbo[user_id][7][0]: lower = "kirbos"
            elif user_kirbo[user_id][7][0] == 5:
                reply_embed = discord.Embed(description="You have max roll cap increases.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
            else:
                user_kirbo[user_id][0] += -(200+100*user_kirbo[user_id][7][0])
                user_kirbo[user_id][7][0] += 1
                reply_embed = discord.Embed(description="You have bought 1 roll cap increase.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
        elif item in ["quality upgrade", "upgrade"]:
            owned = user_kirbo[user_id][7][1]
            if [user_kirbo[user_id][0], user_kirbo[user_id][6][0], user_kirbo[user_id][6][1]][owned] < [300, 200, 200][owned]: lower = ["kirbos", "silver", "gold"][owned]
            elif owned == 3:
                reply_embed = discord.Embed(description="You have max quality upgrades.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
            else:
                if owned == 0: user_kirbo[user_id][0] += -300
                elif owned == 1: user_kirbo[user_id][6][0] += -200
                else: user_kirbo[user_id][6][1] += -200
                user_kirbo[user_id][7][1] += 1
                reply_embed = discord.Embed(description=f"You have bought quality upgrade {owned+1}.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
        elif item in ["cluster research", "cluster"]:
            owned = user_kirbo[user_id][7][2]
            prices = [300, 600, 900, 1200, 1500, 1800, 2100, 2500]
            if user_kirbo[user_id][0] < prices[owned]: lower = "kirbos"
            elif owned == 8:
                reply_embed = discord.Embed(description="You have max cluster research.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
            else:
                user_kirbo[user_id][0] += -(prices[owned])
                user_kirbo[user_id][7][2] += 1
                reply_embed = discord.Embed(description=f"You have bought cluster research {owned+1}.", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
        
        if lower != None:
            reply_embed = discord.Embed(description=f"You do not have emough {lower} to buy this item.", color=0x725628)
            await ctx.reply(embed=reply_embed)
            return

        save(user_kirbo)
    
    @hidden.command(brief="refine items into silver, gold or pure kirbo. list of recipes on full help menu",
                    help="""
                    recipes:

                    silver (kirbo/green kirbo/pink kirbo) + 200 kirbos -> 1 silver
                    silver (easy/normal/hard) + 300 kirbos -> 2 silver
                    silver (harder/insane) + 350 kirbos -> 3 silver
                    silver (easy/medium/hard) demon + 400 kirbos -> 4 silver
                    silver (insane/extreme) demon + 450 kirbos -> 5 silver
                    silver grandpa demon + 500 kirbos -> 10 silver [recipe 1]
                    (10x) silver grandpa demon + 8000 kirbos -> 1 pure kirbo [recipe 2]""")
    async def refine(self, ctx, recipe: typing.Optional[int], *, item: str):
        global user_kirbo
        user_id = str(ctx.author.id)

        qualities = ["silver", "gold", "ultra"]
        items = ["kirbo", "green kirbo", "pink kirbo", "easy", "normal", "hard", "harder", "insane",
                  "easy demon", "medium demon", "hard demon", "insane demon", "extreme demon", "grandpa demon"]
        equal_value = [["blue kirbo", "pink kirbo"], ["normal", "hard"], ["insane"], ["medium demon", "hard demon"], ["extreme demon"]]
        base_value = ["kirbo", "easy", "harder", "easy demon", "insane demon"]
        recipes = {"silver kirbo" : [["s1", 200, 1]], "silver easy" : [["s2", 300, 1]], "silver harder" : [["s3", 350, 1]],
                   "silver easy demon" : [["s4", 400, 1]], "silver insane demon" : [["s5", 450, 1]], "silver grandpa demon" : [["s10", 500, 1], ["p1", 8000, 10]], # silver item -> silver, 10 silver grandpa -> pure kirbo
                   
                   "gold kirbo" : [["g1", 400, 1]], "gold easy" : [["g2", 600, 1]], "gold harder" : [["g3", 700, 1]],
                   "gold easy demon" : [["g4", 800, 1]], "gold insane demon" : [["g5", 900, 1]], "gold grandpa demon" : [["g10", 1000, 1], ["p1", 8000, 5]], # gold item -> gold, 5 gold grandpa -> pure kirbo
                   
                   "ultra kirbo" : [["p1", 2000, 1]], "ultra easy" : [["p2", 3000, 1]], "ultra harder" : [["p3", 3500, 1]],
                   "ultra easy demon" : [["p4", 4000, 1]], "ultra insane demon" : [["p5", 4500, 1]], "ultra grandpa demon" : [["p10", 5000, 1]]} # ultra item -> pure kirbo
        
        item = item.lower()
        quality = "silver" if item.startswith("silver") else "gold" if item.startswith("gold") else "ultra" if item.startswith("ultra") else None
        item = item.replace("silver ", "").replace("gold ", "").replace("ultra ", "")
        full_name = f"{quality} {item}"
        if item not in recipes:
            for equal in equal_value: new_item = base_value[equal_value.index(equal)] if item in equal else item
            if f"silver {new_item}" not in recipes or quality == None:
                reply_embed = discord.Embed(description="That item does not have a recipe, run `c!help hidden refine` for a list of valid recipes", color=0x725628)
                await ctx.reply(embed=reply_embed)
                return
            full_name = f"{quality} {new_item}"
        
        if recipe == None: recipe = 1
        if len(recipes[full_name]) < recipe or recipe < 1:
            reply_embed = discord.Embed(description=f"That item does not have a recipe at index {recipe}", color=0x725628)
            await ctx.reply(embed=reply_embed)
            return
        recipe += -1
        if user_kirbo[user_id][0] < recipes[full_name][recipe][1]:
            reply_embed = discord.Embed(description="You do not have enough kirbos to refine that item", color=0x725628)
            await ctx.reply(embed=reply_embed)
            return
        if user_kirbo[user_id][8][qualities.index(quality)][items.index(item)] < recipes[full_name][recipe][2]:
            reply_embed = discord.Embed(description="You do not have enough of that item", color=0x725628)
            await ctx.reply(embed=reply_embed)
            return
        
        user_kirbo[user_id][0] += -(recipes[full_name][recipe][1])
        user_kirbo[user_id][8][qualities.index(quality)][items.index(item)] += -(recipes[full_name][recipe][2])
        user_kirbo[user_id][6][["s", "g", "p"].index(recipes[full_name][recipe][0][0])] += recipes[full_name][recipe][0][1:]

        reply = f"You have refined {recipes[full_name][recipe][2]} {quality} {item} into {recipes[full_name][recipe][0][1:]} {['silver', 'gold', 'pure kirbo'][['s', 'g', 'p'].index(recipes[full_name][recipe][0][0])]}."
        reply_embed = discord.Embed(description=reply, color=0x725628)
        await ctx.reply(embed=reply_embed)