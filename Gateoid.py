import discord
import json
from discord.ext import commands
import tokens
import ids as ogid

description = '''Gateoid bot for Open Gates on Discord'''
bot = commands.Bot(command_prefix='!', description=description)
client = discord.Client()

### Global subcommands

def getText(name):
    with open("text/{}.txt".format(name), encoding="utf8") as f:
        return f.read()

def checkRoles(member, id):
    for role in member.roles:
        if role.id == id:
            return True
    return False

### Member management
@bot.event
async def on_member_join(member):
    """Welcomes new members."""
    message = getText("welcome").format(member.mention)
    channel = bot.get_channel(ogid.welcome)
    await channel.send(message)
    message = '➕ Yay, {} just joined Open Gates!'.format(member.mention)
    channel = bot.get_channel(ogid.usertraffic)
    await channel.send(message)

@bot.event
async def on_member_remove(member):
    """Informs the moderators when someone leaves."""
    message = '➖ Aww, {} just left Open Gates.'.format(member.mention)
    channel = bot.get_channel(ogid.usertraffic)
    await channel.send(message)

@bot.event
async def on_member_update(before, after):
    if not checkRoles(before, ogid.members) and checkRoles(after, ogid.members):
        await bot.get_channel(ogid.general).send(getText("verified").format(after, ogid.aboutus, ogid.introductions, ogid.botspam))
        await bot.get_channel(ogid.general).send("testing")
        return

### Bot chat
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return    
    await bot.process_commands(message)
    with open('json/chat.json', encoding="utf8") as f:
        keywords = json.loads(f.read())
        
        for keyword in keywords:
            kws = keyword.split(",")
            found = True
            for kw in kws:
                if kw not in message.content:
                    found = False
            if found:
                await message.channel.send(keywords[keyword])
                break

### Automatic creation of channels
@bot.command()
@commands.has_role(ogid.members)
async def topic(ctx, ucc):
        category = None
        for cat in ctx.guild.categories:
            if cat.id == ogid.ucc:
                category = cat
                
        if category is None:
            print("Couldn't grab category")
            return
            
        channel = await ctx.guild.create_text_channel(str(ucc), category=category)
        await channel.send("**{} please let us know what this channel is for! :-)**".format(ctx.message.author.mention, channel.name))

@bot.command()
@commands.has_role(ogid.members)
async def game(ctx, game):
        category = None
        for cat in ctx.guild.categories:
            if cat.id == ogid.games:
                category = cat
                
        if category is None:
            print("Couldn't grab category")
            return
            
        channel = await ctx.guild.create_text_channel(str(game), category=category)
        await channel.send("**{} please let us know what this channel is about! :-)** Share a link to the game, let us know on which platform you play, if you're looking for trades, etc.".format(ctx.message.author.mention, channel.name))
        
@bot.command()
@commands.has_role(ogid.mods)
async def mod(ctx, mcc):
        category = None
        for cat in ctx.guild.categories:
            if cat.id == ogid.mcc:
                category = cat
                
        if category is None:
            print("Couldn't grab category")
            return
            
        channel = await ctx.guild.create_text_channel(str(mcc), category=category)
        await channel.send("**{} please let us know what this channel is for! :-)**".format(ctx.message.author.mention, channel.name))

### Removing messages
def is_pinned(m):
    return not m.pinned
    
async def has_non_pinned(channel):
    async for msg in channel.history():
        if not msg.pinned:
            return True
    return False

@bot.command(help="Clear X messages.")
@commands.has_role(ogid.mods)
async def clear(ctx, amt: int):
    amt += 1
    count = 0
    while amt > 0:
        next = min(1000, amt)
        deleted = await ctx.message.channel.purge(limit=next, check=is_pinned)
        amt -= next
        count += len(deleted)

    message = await ctx.send("🗑️ {} deleted {} messages!".format(ctx.message.author.mention, count - 1))
    await asyncio.sleep(5)
    await message.delete()

### Run bot
@bot.event
async def on_ready():
    game = discord.Game("Animal Crossing: New Horizons")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(bot.user.name + ' is running.')
    
bot.run(tokens.Gateoid)
