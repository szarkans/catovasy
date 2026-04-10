import random

import disnake
from disnake.ext import commands

from bot.storage import names


class MainCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='new', aliases=['новый', 'создать'], description='Создание нового котика')
    async def createNewCat(self, ctx: commands.Context):
        
        if has_cat:
            await ctx.reply("У тебя уже есть котик! Открой его командой `.к кот`")
            return
        new_cat = {
            "title": disnake.ui.TextDisplay("## Новый котик | Создание..."),
            "desc": disnake.ui.TextDisplay("Пол: ...\nИмя: ...\nОкрас: ...\n\nСила: ...\nЗдоровье: ...\nВыносливость: ...\nЗащита: ..."),
        }
        new_cat_container = disnake.ui.Container(
            *new_cat.values()
        )
        gender = random.choice(["male", "female"])
        name = random.choice(names["gender"])
        color = 



def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))