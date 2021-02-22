#! python3
# randomamongus.py

"""
==============================================================================
MIT License

Copyright (c) 2020 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
"""

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
        self.maps = ["Airship", "MIRA HQ", "Polus", "The Skeld"]

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
        mapname = random.choice(self.maps)
        embed = discord.Embed(title="Randomize Map", color=0xff0000)
        embed.add_field(name="Map", value=mapname)
        embed.add_field(name="Impostors", value=str(random.randint(1, 3)))
        thumbnail = f"{''.join(mapname.split()).lower()}.png"
        embed.set_thumbnail(url=f"attachment://{thumbnail}")
        await ctx.channel.send(
            file=discord.File(os.path.join('data', thumbnail), thumbnail),
            embed=embed
        )

    @commands.command(name="randsettings", pass_context=True, aliases=["rs"])
    async def randsettings(self, ctx, setting=''):
        """ Select random option for specified setting
            <setting> can be any of the settings which can be modified in-lobby
            Leaving <setting> blank will randomize all settings
"""
        setting = setting.title()
        fields = {}
        if self.settings.get(setting) is None:
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
