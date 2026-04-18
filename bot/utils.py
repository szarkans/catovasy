import datetime
import random
import uuid

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
            has_cat = await conn.execute("SELECT 1 FROM cats WHERE owner_ds_id = $1", discord_id)
        elif uuid:
            has_cat = await conn.execute("SELECT 1 FROM cats WHERE uuid = $1", uuid)
        else:
            raise ValueError
            return
        if has_cat:
            status = await conn.fetchval("SELECT status FROM cats WHERE owner_ds_id = $1", discord_id)
            if status == "pending":
                return True
            else:
                return True
        return False
    

async def newCat(pool: asyncpg.Pool,
                owners_ds_id: int,
                guild_id: int,
                name: str,
                gender: str,
                color: str,
                base_attack: float,
                base_defense: float,
                base_endurance: float,
                base_hp: int,
                ) -> str:
    cat_uuid = str(uuid.uuid4())
    tz = datetime.timezone(datetime.timedelta(hours=3))
    last_interaction = datetime.datetime.now(tz=tz)
    created_at = datetime.datetime.now(tz=tz)

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                INSERT INTO cats (
                    uuid, owner_ds_id, guild_id, name, gender, color,
                    balance,
                    base_attack, attack_mod,
                    base_defense, defense_mod,
                    base_endurance, endurance_mod,
                    base_hp, hp_mod, current_hp,
                    status, age,
                    last_grow_action_time, last_interaction_time,
                    downed_until, custom_data, created_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6,
                    0,
                    $7, 0,
                    $8, 0,
                    $9, 0,
                    $10, 0, $10,
                    'afk', 0,
                    NULL, $11,
                    NULL, $12, $13
                )
                """,
                cat_uuid, owners_ds_id, guild_id, name, gender, color,
                base_attack,
                base_defense,
                base_endurance,
                base_hp,
                last_interaction,
                None, created_at,
            )
            await conn.execute("INSERT INTO inventories (cat_uuid) VALUES ($1)", cat_uuid,)
    return cat_uuid
