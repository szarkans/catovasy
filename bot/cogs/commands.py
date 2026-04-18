import asyncio
import random

import disnake
from disnake.ext import commands

from bot.storage import names, colors
from bot.utils import catExists, newCat
from bot.bot import Bot


class MainCommands(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='new', aliases=['новый', 'создать'], description='Создание нового котика')
    async def createNewCat(self, ctx: commands.Context):
        
        # if await catExists(self.bot.pool, ctx.author.id):
        #     await ctx.reply("У тебя уже есть котик! Открой его командой `.к кот`")
        #     return
        new_cat = {
            "title": disnake.ui.TextDisplay("## Новый котик | Создание..."),
            "desc": disnake.ui.TextDisplay("Пол: ...\nИмя: ...\nОкрас: ...\n\nСила: ...\nЗдоровье: ...\nВыносливость: ...\nЗащита: ..."),
        }
        new_cat_container = disnake.ui.Container(
            *new_cat.values()
        )
        cont = await ctx.send(components=new_cat_container)
        gender = random.choice(["male", "female"])
        name = random.choice(names[gender])
        color = random.choice(list(colors.keys()))
        base_attack = round(random.uniform(0.5, 2.0), 2)
        base_defense = round(random.uniform(0.5, 2.0), 2)
        base_endurance = round(random.uniform(0.5, 2.0), 2)
        base_hp = random.randint(1, 3)
        await newCat(self.bot.pool,
                    ctx.author.id,
                    ctx.guild.id,
                    name,gender,color,base_attack,base_defense,base_endurance,
                    base_hp)
        await asyncio.sleep(3)
        new_cat = {
            "title": disnake.ui.TextDisplay("## Новый котик!"),
            "desc": disnake.ui.TextDisplay(f"Пол: {gender}\nИмя: {name}\nОкрас: {color}\n\nСила: {base_attack}\nЗдоровье: {base_hp}\nВыносливость: {base_endurance}\nЗащита: {base_defense}"),
        }
        new_cat_container = disnake.ui.Container(
            *new_cat.values()
        )
        await cont.edit(components=new_cat_container)



def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))