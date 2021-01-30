#! python3
# randomamongus.py

import json
import random
import os

import discord
from discord.ext import commands


class RandomAmongUs(commands.Cog):
    """ Generate a random option for various categories in Among Us
"""
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.join('data', 'settings.txt')) as file:
            self.settings = json.load(file)
        self.maps = ["MIRA HQ", "Polus", "The Skeld"]

    @commands.command(name="randomize", pass_context=True, aliases=["r"])
    async def randomize(self, ctx):
        """ Invoke all commands in RandomAmongUs
"""
        for cmd in self.get_commands():
            if cmd.name == "randomize":
                continue
            await ctx.invoke(cmd)

    @commands.command(name="randmap", pass_context=True, aliases=["rm"])
    async def randmap(self, ctx):
        """ Select random map
"""
        num = random.randint(1, 3)
        mapname = random.choice(self.maps)
        embed = discord.Embed(title="Randomize Map", color=0xff0000)
        embed.add_field(name="Map", value=mapname)
        embed.add_field(name="Impostors", value=str(num))
        thumb_name = f"{''.join(mapname.split()).lower()}.png"
        thumb_path = os.path.join(
            'data', thumb_name)
        thumbnail = discord.File(thumb_path, thumb_name)
        embed.set_thumbnail(url=f"attachment://{thumb_name}")
        await ctx.channel.send(file=thumbnail, embed=embed)

    @commands.command(name="randsettings", pass_context=True, aliases=["rs"])
    async def randsettings(self, ctx, setting=''):
        """ Select random option for specified setting
            <setting> can be any of the settings which can be modified in-lobby
            Leaving <setting> blank will randomize all settings
"""
        setting = setting.title()
        options = self.settings.get(setting)
        fields = {}
        if options is None:
            title = "Randomize Setting: ALL"
            for opt in self.settings:
                fields.setdefault(opt, random.choice(self.settings[opt]))
        else:
            title = f"Randomize Setting: {setting}"
            fields.setdefault(setting, random.choice(self.settings[setting]))
        embed = discord.Embed(title=title, color=0xff0000)
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        await ctx.send(embed=embed)


def setup(bot):
    """ Allow lib.bot.__init__.py to add RandomAmongUs cog
"""
    bot.add_cog(RandomAmongUs(bot))
