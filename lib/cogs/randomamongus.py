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
    """ Generates random aspects of Among Us
"""
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.join('data', 'settings.txt')) as file:
            self.settings = json.load(file)
        self.maps = ["Airship", "MIRA HQ", "Polus", "The Skeld"]

    @commands.command(name="randomize", pass_context=True, aliases=["r"])
    async def randomize(self, ctx):
        """ Invokes all commands in RandomAmongUs cog
"""
        # Invoke randmap and ransettings command
        await ctx.invoke(self.bot.get_command("randmap"))
        await ctx.invoke(self.bot.get_command("randsettings"))

    @commands.command(name="randmap", pass_context=True, aliases=["rm"])
    async def randmap(self, ctx):
        """ Selects random Among Us map
"""
        # Choose a random map
        mapname = random.choice(self.maps)
        # Construct an embed to send data
        embed = discord.Embed(title="Randomize Map", color=0xff0000)
        # Add name of map as embed field
        embed.add_field(name="Map", value=mapname)
        # Add random number of impostors as embed field
        embed.add_field(name="Impostors", value=str(random.randint(1, 3)))
        # Set thumbnail to map logo
        thumbnail = f"{''.join(mapname.split()).lower()}.png"
        embed.set_thumbnail(url=f"attachment://{thumbnail}")
        # Send constructed embed
        await ctx.channel.send(
            file=discord.File(os.path.join('data', thumbnail), thumbnail),
            embed=embed
        )

    @commands.command(name="randsettings", pass_context=True, aliases=["rs"])
    async def randsettings(self, ctx, setting=''):
        """ Selects random option for specified setting
            <setting> can be any of the settings which can be modified in-lobby
            Leaving <setting> blank will randomize all settings
"""
        setting = setting.title()
        fields = {}
        # Generate random option for all in-lobby settings
        if self.settings.get(setting) is None:
            title = "Randomize Setting: ALL"
            for opt in self.settings:
                fields.setdefault(opt, random.choice(self.settings[opt]))
        # Generate random option for setting
        else:
            title = f"Randomize Setting: {setting}"
            fields.setdefault(setting, random.choice(self.settings[setting]))
        # Construct embed to send data
        embed = discord.Embed(title=title, color=0xff0000)
        # Add randomized option as embed field
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        # Send constructed embed
        await ctx.channel.send(embed=embed)

    @commands.command(name="listsettings", pass_context=True, aliases=["lset"])
    async def listsettings(self, ctx):
        """ Lists the in-lobby settings in Among Us
"""
        # Create embed description to list of settings
        desc = "\n".join([f"- {s}" for s in self.settings])
        # Construct embed to send data
        embed = discord.Embed(
            title="In-Lobby Settings", description=desc, color=0xff0000
        )
        # Send constructed embed
        await ctx.channel.send(embed=embed)


def setup(bot):
    """ Adds RandomAmongUs cog
"""
    bot.add_cog(RandomAmongUs(bot))
