#!usr/bin/env python3
#-*-coding:utf-8-*-

from src.discord.checks import *
from discord.ext import commands
import logging
import sys
import asyncio

class BotManage(commands.Cog, name="Bot Management", command_attrs=dict(hidden=True)):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_botowner)
    @commands.command(aliases=["eval"])
    async def debug(self, ctx, *, arg):
        self.logger.log(logging.DEBUG+1, "running debug instruction : %s", arg.replace("```python", "").replace("```", ""))
        exec(arg.replace("```python", "").replace("```", ""))

    @commands.check(check_botowner)
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.channel.send("You are requesting a shutdown, please ensure that you want to performe it by typing `confirm`")
        chk = lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'confirm'
        try: answer = await self.bot.wait_for('message', check=chk, timeout=60)
        except asyncio.TimeoutError: answer = None
        if answer is None:
            await ctx.channel.send("your request has timeout")
        else:
            self.logger.warning("Shutdown requested by %s", str(ctx.author))
            await self.bot.close()
            sys.exit(0)
