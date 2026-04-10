import random

import asyncpg
import disnake

async def catExists(pool: asyncpg.Pool, discord_id: int = None, uuid: str = None) -> str:
    """Узнаёт существует ли котик на дискорд юзере или есть ли такой котик по uuid

    Args:
        pool (_type_): connection pool to postgre
        discord_id (int, optional): discord_id. Defaults to None.
        uuid (str, optional): uuid кота. Defaults to None.

    Raises:
        ValueError: Если не передали ни дискорд айди ни uuid

    Returns:
        str: true/false/pending (есть котик, нет котика, котик в процессе создания)
    """
    async with pool.acquire() as conn:
        if discord_id:
            has_cat = await conn.execute("SELECT 1 FROM cats WHERE discord_id = $1", (discord_id,))
        elif uuid:
            has_cat = await conn.execute("SELECT 1 FROM cats WHERE uuid = $1", (uuid,))
        else:
            raise ValueError
            return
        if has_cat:
            status = await conn.fetchval("SELECT status FROM cats WHERE discord_id = $1", (discord_id,))
            if status == "pending":
                return "pending"
            else:
                return "true"
        return "false"
