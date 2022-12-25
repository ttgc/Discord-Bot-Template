#!usr/bin/env python3
#-*-coding:utf-8-*-

import discord.utils

def check_servowner(ctx):
    return discord.utils.get(ctx.guild.roles, id=ctx.author == ctx.guild.owner)

async def check_botowner(ctx): 
    return ctx.bot.is_owner(ctx.author)

# Define custom checks below
