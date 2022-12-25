#!usr/bin/env python3
#-*-coding:utf-8-*-

# import external and python libs
import discord
from discord.ext import commands
import asyncio
import traceback

# import custom libs
from src.setup.config import *
from src.setup.inits import *

# import Cogs
from src.discord.cogs.BotManage import *

# Initialize logs
global logger
logger = initlogs()

# Initialize bot status
global statut
statut = discord.Game(name=Config()["discord"]["default-game"])

# Get bot Token
global TOKEN
TOKEN = Config()["token"]

# Get prefix function
def get_prefix(bot, message):
    return Config()["discord"]["default-prefix"]

# Initialize client
global client
client = discord.ext.commands.Bot(get_prefix, case_insensitive=True, activity=statut, intents=discord.Intents.all())

# Global checks
@client.check
def no_pm(ctx): return ctx.guild is not None

@client.check
def isbot(ctx): return not ctx.author.bot

# Client events
@client.event
async def on_command_error(ctx, error):
    global logger
    msg = f"error occured: ```{error}```"

    if isinstance(error, commands.CheckFailure): return
    else: logger.warning(error)
    await ctx.message.channel.send(msg)

@client.event
async def on_error(event, *args, **kwargs):
    global logger
    logger.error(traceback.format_exc())


@client.event
async def on_connect():
    global logger
    if len(client.cogs) > 0: return

    await client.add_cog(BotManage(client, logger))

    test_guild = Config()['discord']['test-guild']
    if test_guild is not None:
        logger.info("Test guild provided. Copying global command to test guild.")
        client.tree.copy_global_to(guild=discord.Object(id=test_guild))

    await client.tree.sync()

@client.event
async def on_ready():
    global statut, logger
    logger.info("Successful connected. Initializing bot system")
    botaskperm = discord.Permissions().all()
    botaskperm.administrator = botaskperm.manage_channels = botaskperm.manage_guild = botaskperm.manage_webhooks = botaskperm.manage_emojis = botaskperm.manage_nicknames = botaskperm.move_members = False
    url = discord.utils.oauth_url(client.user.id, permissions=botaskperm)
    logger.info("Generated invite link : %s", url)
    logger.info("Bot is now ready")

# ========== MAIN ========== #
def main():
    client.run(Config()["token"])

# Launch the bot
if __name__ == "__main__":
    main()
