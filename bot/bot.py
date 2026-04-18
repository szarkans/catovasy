import asyncpg
import disnake
from disnake.ext import commands

import os

os.environ["PYTHONIOENCODING"] = "UTF-8"

intents = disnake.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=disnake.Intents.all(),
            command_prefix='.к',
            reload=True,
            command_sync_flags=commands.CommandSyncFlags.all(),
            strip_after_prefix=True,
            test_guilds=[1138425078493753366],
            owner_id=531208170098655233
        )
        self.pool: asyncpg.Pool = None

    async def close(self):
        if self.pool:
            await self.pool.close()
        await super().close()

    async def on_ready(self):
        print("Я родился!")
        self.pool = await asyncpg.create_pool(
            dsn=os.getenv("DATABASE_URL"),
            min_size=2,
            max_size=10,
            statement_cache_size=0,
        )
        print("БД подключена")

bot = Bot()