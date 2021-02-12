#! python3
# mapdatabase.py

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

import asyncio
import os
import re
import sqlite3

import discord
from discord.ext import commands


class MapDatabase(commands.Cog):
    """ Allow member to explore available information in Among Us
"""
    def __init__(self, bot):
        self.bot = bot
        self.arship_parser = DatabaseParser(self.bot.airship, self.bot)
        self.mira_hq_parser = DatabaseParser(self.bot.mirahq, self.bot)
        self.polus_parser = DatabaseParser(self.bot.polus, self.bot)
        self.the_skeld_parser = DatabaseParser(self.bot.theskeld, self.bot)

    @commands.group(
        name="Airship", case_insensitive=True, pass_context=True,
        aliases=["A"]
    )
    async def airship(self, ctx):
        """ Command group to parse data/db/airship.sqlite
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Airship command passed")

    @airship.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def airship_retrieve(self, ctx, category, option):
        """ Retrieve option for category in Airship database
"""
        await self.arship_parser.retrieve(ctx, category, option)

    @airship.group(
        name="search", case_insensitive=True, pass_context=True,
        aliases=["s"]
    )
    async def airship_search(self, ctx, category):
        """ Search options for category in Airship database
"""
        await self.arship_parser.search(ctx, category)

    @airship.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def airship_listopts(self, ctx, category):
        """ List options for category in Airship database
"""
        await self.arship_parser.listopts(ctx, category)

    @commands.group(
        name="MIRAHQ", case_insensitive=True, pass_context=True,
        aliases=["MIRA", "MH"]
    )
    async def mira_hq(self, ctx):
        """ Command group to parse data/db/mira_hq.sqlite
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid MIRA HQ command passed")

    @mira_hq.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def mirahq_retrieve(self, ctx, category, option):
        """ Retrieve option for category in MIRA HQ database
"""
        await self.mira_hq_parser.retrieve(ctx, category, option)

    @mira_hq.group(
        name="search", case_insensitive=True, pass_context=True,
        aliases=["s"]
    )
    async def mirahq_search(self, ctx, category):
        """ Search options for category in MIRA HQ database
"""
        await self.mira_hq_parser.search(ctx, category)

    @mira_hq.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def mirahq_listopts(self, ctx, category):
        """ List options for category in MIRA HQ database
"""
        await self.mira_hq_parser.listopts(ctx, category)

    @commands.group(
        name="Polus", case_insensitive=True, pass_context=True,
        aliases=["P"]
    )
    async def polus(self, ctx):
        """ Command group to parse data/db/polus.sqlite
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Polus command passed")

    @polus.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def polus_retrieve(self, ctx, category, option):
        """ Retrieve option for category in Polus database
"""
        await self.polus_parser.retrieve(ctx, category, option)

    @polus.group(
        name="search", case_insensitive=True, pass_context=True,
        aliases=["s"]
    )
    async def polus_search(self, ctx, category):
        """ Search options for category in Polus database
"""
        await self.polus_parser.search(ctx, category)

    @polus.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def polus_listopts(self, ctx, category):
        """ List options for category in Polus database
"""
        await self.polus_parser.listopts(ctx, category)

    @commands.group(
        name="TheSkeld", case_insensitive=True, pass_context=True,
        aliases=["Skeld", "TS"]
    )
    async def the_skeld(self, ctx):
        """ Command group to parse data/db/theskeld.sqlite
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid The Skeld command passed")

    @the_skeld.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def theskeld_retrieve(self, ctx, category, option):
        """ Retrieve option for category in The Skeld database
"""
        await self.the_skeld_parser.retrieve(ctx, category, option)

    @the_skeld.group(
        name="search", case_insensitive=True, pass_context=True,
        aliases=["s"]
    )
    async def theskeld_search(self, ctx, category):
        """ Search options for category in The Skeld database
"""
        await self.the_skeld_parser.search(ctx, category)

    @the_skeld.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def theskeld_listopts(self, ctx, category):
        """ List options for category in The Skeld database
"""
        await self.the_skeld_parser.listopts(ctx, category)


class DatabaseParser:
    """ Parse SQLite databases in data/db
"""
    def __init__(self, database, bot):
        self.database = database
        self.bot = bot

    async def retrieve(self, ctx, category, option):
        """ Retrieve a specific option from a category of options
"""
        category, option = category.lower(), option.title()
        query = f"""
                SELECT *
                FROM {category}
                WHERE name=?
                """
        try:
            columns, content = self.database.execute_query(query, "rr", option)
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        data = dict(zip(columns, content[0]))
        if not data:
            await ctx.channel.send("No results found.")
        # Send data in embed
        embed = discord.Embed(
            title=f"{category.title()}: {option}", color=0xff0000
        )
        for item in data:
            embed.add_field(name=item.title(), value=data[item])
        embed.set_footer(text=ctx.command.full_parent_name)
        image_name = f"{data['name']}.png"
        image_path = os.path.join(
            "data", ctx.command.full_parent_name.lower(), category, image_name
        )
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)

    async def search(self, ctx, category):
        """ Allow member to scroll through options for category of map
"""
        # Get data from database
        category = category.lower()
        query = f"""
        SELECT *
        FROM {category}
        """
        try:
            columns, content = self.database.execute_query(query, "rr")
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        if not (columns or content):
            await ctx.send(f"No results found [`category`={category}]")
            return
        data = {
            d["name"]: d for d in [dict(zip(columns, c)) for c in content]
        }
        # Create embed for member to scroll data with
        embed, image = scrolling_embed(
            ctx.command.full_parent_name, category, data
        )
        message = await send_with_reactions(ctx, embed, image)
        while True:
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add", timeout=30.0,
                    check=lambda p: p.member.id == ctx.author.id
                )
                if payload.emoji.name in [
                    u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9',
                    u'\u23ed'
                ]:
                    await self.scroll(payload, data)
                elif payload.emoji.name == u'\u2714':
                    await self.retrieve_from_search(payload, data)
                elif payload.emoji.name == u'\u274c':
                    await self.delete_search(payload)
            except asyncio.TimeoutError:
                break
        await message.clear_reactions()
        await message.delete()

    async def listopts(self, ctx, category):
        """ List all options for a category of map
"""
        # Get data from database
        category = category.lower()
        query = f"""
        SELECT *
        FROM {category}
        """
        try:
            content = self.database.execute_query(query, "r")
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        if not content:
            await ctx.channel.send("No results found.")
            return
        # Send data in embed
        embed = discord.Embed(
            title=category.title(), color=0xff0000,
            description='\n'.join([f"-{r[0]}" for r in content])
        )
        embed.set_footer(text=ctx.command.full_parent_name)
        await ctx.channel.send(embed=embed)

    async def retrieve_from_search(self, payload, data):
        """ Retrieve data for current option of embed
"""
        # Process payload information
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        # Get current option information from embed
        footer_regex = re.compile(
            r"(Airship|MIRAHQ|Polus|TheSkeld)",
            re.IGNORECASE
        )
        title_regex = re.compile(r"^(.*): (.*)")
        mapname = footer_regex.search(embed.footer.text).group(1)
        category = title_regex.search(embed.title).group(1)
        option = title_regex.search(embed.title).group(2)
        # Edit embed to mimic retrieve command
        embed = discord.Embed(
            title=f"{category}: {option}", color=0xff0000
        )
        for item in data[option]:
            embed.add_field(
                name=item.title(), value=data[option][item]
            )
        embed.set_footer(text=mapname)
        image_name = f"{option}.png"
        image_path = os.path.join(
            'data', mapname.lower(), category.lower(), image_name
        )
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await channel.send(file=image, embed=embed)
        await message.delete()

    async def scroll(self, payload, data):
        """ Scroll embed from search command based on the emoji used
"""
        # Process payload information
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        # Get current option information from embed
        footer_regex = re.compile(
            r"(Airship|MIRAHQ|Polus|TheSkeld)",
            re.IGNORECASE
        )
        title_regex = re.compile(
            r"^(.*): (.*)"
        )
        mapname = footer_regex.search(embed.footer.text).group(1)
        category = title_regex.search(embed.title).group(1)
        option = title_regex.search(embed.title).group(2)
        # Get current index and scroll appropriately
        index = list(data).index(option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index - 5, u'\u25c0': index - 1,
            u'\u25b6': index + 1, u'\u23e9': index + 5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name) % len(data)
        embed = scrolling_embed(
            mapname, category, data, index=index
        )[0]
        await message.edit(embed=embed)
        await message.remove_reaction(payload.emoji, payload.member)

    async def delete_search(self, payload):
        """ Delete embed from search command
"""
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.delete()


def scrolling_embed(mapname, category, data, *, index=0):
    """ Create and embed to allow member to scroll data with
"""
    # Get current option data
    option_data = list(data.values())[index]
    # Send data in embed
    embed = discord.Embed(
        title=f"{category.title()}: {option_data['name']}",
        color=0xff0000
    )
    embed.set_footer(
        text=f"{mapname}: Page {index+1}/{len(data)}"
    )
    for item in option_data:
        embed.add_field(
            name=item.title(),
            value=option_data[item]
        )
    # Attach map logo image
    image_name = f"{mapname.lower()}.png"
    image_path = os.path.join('data', image_name)
    image = discord.File(image_path, image_name)
    embed.set_image(url=f"attachment://{image_name}")
    return embed, image


async def send_with_reactions(ctx, embed, image):
    """ Send message with reactions for member to scroll data with
"""
    # Send image and embed
    message = await ctx.channel.send(
        file=image, embed=embed
    )
    # Add scroll control reactions
    reactions = [
        u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
        u'\u2714', u'\u274c'
    ]
    for rxn in reactions:
        await message.add_reaction(rxn)
    return message


def setup(bot):
    """ Add MapDatabase cog
"""
    bot.add_cog(MapDatabase(bot))
