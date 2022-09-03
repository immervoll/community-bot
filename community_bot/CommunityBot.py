import asyncio
import logging
import logging.handlers
import os


from typing import List, Optional

from common.settings import Settings

import discord
from discord.ext import commands
from aiohttp import ClientSession

class CommunityBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.

    

async def main():
    
    # settings setup
    
    settings = Settings()
    
    # logging Setup
    logger = logging.getLogger('discord')
    logger.setLevel(settings._bot_log_level)

    handler = logging.handlers.RotatingFileHandler(
        filename=settings._bot_log_file,
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # bot setup
    async with CommunityBot(commands.when_mentioned, initial_extensions=settings._bot_modules) as bot:
        await bot.start(settings._bot_token)



asyncio.run(main())
