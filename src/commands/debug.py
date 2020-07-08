"""
debug.py - Debug and diagnostics commands

Provides IRC commands geared towards debugging mechasqueak itself.
This module should **NOT** be loaded in a production environment

Copyright (c) 2018 The Fuel Rat Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
from uuid import UUID

from src.config import PLUGIN_MANAGER
from src.packages.commands import command
from src.packages.context.context import Context
from src.packages.permissions.permissions import require_permission, TECHRAT, require_channel
from loguru import logger


@command("debug-whois")
@require_channel
@require_permission(TECHRAT)
async def cmd_debug_whois(context):
    """A debug command for running a WHOIS command.

    Returns
        str: string repreentation
    """
    data = await context.bot.whois(context.words[1])
    logger.debug(data)
    await context.reply(f"{data}")


@command("debug-userinfo")
@require_permission(TECHRAT)
@require_channel
async def cmd_debug_userinfo(context: Context):
    """
    A debug command for getting information about a user.
    """

    await context.reply(f"triggering user is {context.user.nickname}, {context.user.hostname}")
    await context.reply(f"user identifed?: {context.user.identified}")


@command("superPing!")
@require_channel
@require_permission(TECHRAT)
async def cmd_superping(context: Context):
    """
    A debug command to coerce mecha to respond.
    """

    await context.reply("pong!")


@command("getConfigPlugins")
@require_channel
@require_permission(TECHRAT)
async def cmd_get_plugins(context: Context):
    """Lists configuration plugins"""
    await context.reply(f"getting plugins...")

    plugins = PLUGIN_MANAGER.list_name_plugin()
    names = [plugin[0] for plugin in plugins]
    await context.reply(",".join(names))


@command("get_nickname_api")
@require_channel
@require_permission(TECHRAT)
async def cmd_get_nickname(context: Context):
    await context.reply("fetching....")
    result = await  context.bot.api_handler.get_rat("ClappersClappyton")
    await context.reply("got a result!")
    logger.debug("got nickname result {!r}", result)


@command("debug_ratid")
@require_channel
@require_permission(TECHRAT)
async def cmd_ratid(context: Context):
    target = context.words[-1]
    await context.reply(f"acquiring ratids for {target!r}...")
    api_rats = await context.bot.api_handler.get_rat(target)
    await context.reply(",".join([f"{rat.uuid}" for rat in api_rats]))


@command("debug_get_rat")
@require_channel
@require_permission(TECHRAT)
async def cmd_debug_get_rat(context: Context):
    target = context.words[-1]
    try:
        target = UUID(target)
    except ValueError:
        return await context.reply("invalid uuid.")
    await context.reply(f"fetching uuid {target}...")
    subject = await context.bot.api_handler.get_rat(target)
    await context.reply(f"{subject} rats returned.")


@command("debug_summoncase")
@require_channel
@require_permission(TECHRAT)
async def cmd_debug_summoncase(context: Context):
    await context.reply("summoning case....")
    rescue = await context.bot.board.create_rescue(client="some_client")
    something = await context.bot.api_handler.create_rescue(rescue)
    await context.reply("done.")
