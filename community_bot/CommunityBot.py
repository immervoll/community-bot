import asyncio
import logging
import logging.handlers
import os


from typing import List, Optional

from community_bot.common.settings import Settings

import discord
from discord.ext import commands
from aiohttp import ClientSession


class CommunityBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        logger: logging.Logger,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.logger = logger

    async def setup_hook(self) -> None:

        for extension in self.initial_extensions:
            await self.load_extension(f"community_bot.modules.{extension}")

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        

async def main():
    
    

    # settings setup

    settings = Settings()

    # logging Setup
    logger = logging.getLogger('discord')
    logger.setLevel(settings._bot_log_level)
    bot_logger = logging.getLogger('community-bot')
    bot_logger.setLevel(settings._bot_log_level)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=settings._bot_log_file,
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    console_handler = logging.StreamHandler()
    
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    bot_logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(console_handler)
    bot_logger.info('CommunityBot starting up')
    
    
    # bot setup
    intents = discord.Intents.default()
    intents.members = True
    #intents.message_content = True
    
    
    #async with CommunityBot(initial_extensions=settings._bot_modules, command_prefix=settings._bot_prefix, intents=intents) as bot:
    #    await bot.start(token = settings._bot_token)
    
    
    bot = CommunityBot(initial_extensions=settings._bot_modules, command_prefix=settings._bot_prefix, intents=intents, logger=bot_logger)
    await bot.start(settings._bot_token)
