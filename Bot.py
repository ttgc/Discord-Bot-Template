#!usr/bin/env python3
#-*-coding:utf-8-*-

# import external and python libs
import discord
from discord.ext import commands
import asyncio
import logging
import traceback
import os
import sys

# import custom libs
from src.setup.config import *
from src.setup.inits import *

# import Cogs
from src.discord.cogs.BotManage import *

# Initialize logs
global logger
logger = initlogs()

# Check bot directories and files
initdirs(logger)
checkfiles(logger)

# Initialize bot status
global statut
statut = discord.Game(name=Config()["discord"]["default-game"])

# Get bot Token
global TOKEN
TOKEN = Config()["token"]

# Get prefix function
def get_prefix(bot,message):
    return Config()["discord"]["default-prefix"]

# Initialize client
global client
client = discord.ext.commands.Bot(get_prefix, case_insensitive=True, activity=statut, help_command=Help(), intents=discord.Intents.all())

# Global checks
@client.check
def no_pm(ctx): return ctx.message.guild is not None

@client.check
def isbot(ctx): return not ctx.message.author.bot

# Client events
@client.event
async def on_command_error(ctx, error):
    global logger
    msg = f"error occured: ```{error}```"

    if isinstance(error,commands.CheckFailure): return
    else: logger.warning(error)
    await ctx.message.channel.send(msg)

@client.event
async def on_error(event, *args, **kwargs):
    global logger
    logger.error(traceback.format_exc())

@client.event
async def on_ready():
    global statut, logger
    logger.info("Successful connected. Initializing bot system")
    botaskperm = discord.Permissions().all()
    botaskperm.administrator = botaskperm.manage_channels = botaskperm.manage_guild = botaskperm.manage_webhooks = botaskperm.manage_emojis = botaskperm.manage_nicknames = botaskperm.move_members = False
    url = discord.utils.oauth_url(client.user.id, botaskperm)
    print(url)
    logger.info("Bot is now ready")

# ========== MAIN ========== #
async def main():
    global TOKEN, logger
    client.add_cog(BotManage(client, logger))
    await client.login(TOKEN)
    await client.connect()

# Launch the bot
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
