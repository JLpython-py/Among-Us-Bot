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
    """ Allows member to explore available information in Among Us
"""
    def __init__(self, bot):
        self.bot = bot
        self.arship_parser = DatabaseParser(self.bot.airship, self.bot)
        self.mira_hq_parser = DatabaseParser(self.bot.mirahq, self.bot)
        self.polus_parser = DatabaseParser(self.bot.polus, self.bot)
        self.the_skeld_parser = DatabaseParser(self.bot.theskeld, self.bot)

    def commands_locked(self, ctx):
        """ Checks if commands are locked for member
"""
        voicechannelcontrol = self.bot.get_cog("VoiceChannelControl")
        return voicechannelcontrol.check_commands(ctx)

    @commands.group(
        name="Airship", case_insensitive=True, pass_context=True,
        aliases=["A"]
    )
    async def airship(self, ctx):
        """ Command group to parse Airship database
"""
        if self.commands_locked(ctx):
            raise commands.CheckFailure
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Airship command passed")

    @airship.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def airship_retrieve(self, ctx, category, option):
        """ Retrieves option for category in Airship database
"""
        await self.arship_parser.retrieve(ctx, category, option)

    @airship.group(
        name="browse", case_insensitive=True, pass_context=True,
        aliases=["search", "b", "s"]
    )
    async def airship_browse(self, ctx, category):
        """ Allows member to browse data stored in Airship database
"""
        await self.arship_parser.browse(ctx, category)

    @airship.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def airship_listopts(self, ctx, category):
        """ Returns a list of options in Airship database for category
"""
        await self.arship_parser.listopts(ctx, category)

    @commands.group(
        name="MIRAHQ", case_insensitive=True, pass_context=True,
        aliases=["MIRA", "MH"]
    )
    async def mira_hq(self, ctx):
        """ Command group to parse MIRA HQ database
"""
        if self.commands_locked(ctx):
            raise commands.CheckFailure
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid MIRA HQ command passed")

    @mira_hq.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def mirahq_retrieve(self, ctx, category, option):
        """ Retrieves option for category in MIRA HQ database
"""
        await self.mira_hq_parser.retrieve(ctx, category, option)

    @mira_hq.group(
        name="browse", case_insensitive=True, pass_context=True,
        aliases=["search", "b", "s"]
    )
    async def mirahq_browse(self, ctx, category):
        """ Allows member to browse data stored in Airship database
"""
        await self.mira_hq_parser.browse(ctx, category)

    @mira_hq.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def mirahq_listopts(self, ctx, category):
        """ Returns a list of options for category in MIRA HQ database
"""
        await self.mira_hq_parser.listopts(ctx, category)

    @commands.group(
        name="Polus", case_insensitive=True, pass_context=True,
        aliases=["P"]
    )
    async def polus(self, ctx):
        """ Command group to parse Polus database
"""
        if self.commands_locked(ctx):
            raise commands.CheckFailure
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Polus command passed")

    @polus.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def polus_retrieve(self, ctx, category, option):
        """ Retrieves option for category in Polus database
"""
        await self.polus_parser.retrieve(ctx, category, option)

    @polus.group(
        name="browse", case_insensitive=True, pass_context=True,
        aliases=["search", "b", "s"]
    )
    async def polus_browse(self, ctx, category):
        """ Allows member to browse data stored in Polus database
"""
        await self.polus_parser.browse(ctx, category)

    @polus.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def polus_listopts(self, ctx, category):
        """ Returns a list of options for category in Polus database
"""
        await self.polus_parser.listopts(ctx, category)

    @commands.group(
        name="TheSkeld", case_insensitive=True, pass_context=True,
        aliases=["Skeld", "TS"]
    )
    async def the_skeld(self, ctx):
        """ Command group to parse The Skeld database
"""
        if self.commands_locked(ctx):
            raise commands.CheckFailure
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid The Skeld command passed")

    @the_skeld.group(
        name="retrieve", case_insensitive=True, pass_context=True,
        aliases=["r"]
    )
    async def theskeld_retrieve(self, ctx, category, option):
        """ Retrieves option for category in The Skeld database
"""
        await self.the_skeld_parser.retrieve(ctx, category, option)

    @the_skeld.group(
        name="browse", case_insensitive=True, pass_context=True,
        aliases=["search", "b", "s"]
    )
    async def theskeld_browse(self, ctx, category):
        """ Allows member to browse data stored in The Skeld database
"""
        await self.the_skeld_parser.browse(ctx, category)

    @the_skeld.group(
        name="listopts", case_insensitive=True, pass_context=True,
        aliases=["ls"]
    )
    async def theskeld_listopts(self, ctx, category):
        """ Returns a list of options for category in The Skeld database
"""
        await self.the_skeld_parser.listopts(ctx, category)

    @airship.error
    @mira_hq.error
    @polus.error
    @the_skeld.error
    async def locked_commands_error(self, ctx, error):
        """ Handles failed check in command group

            Occurrence:
            - Member is in a voice channel which has been claimed
            - Member in control of voice channel locks MapDatabase commands
            - Member attempted to invoke a MapDatabase command
"""
        if isinstance(error, commands.CheckFailure):
            message = await ctx.channel.send(
                "`MapDatabase` commands are locked."
            )
            await ctx.message.delete()
            await asyncio.sleep(10)
            await message.delete()


class DatabaseParser:
    """ Parses SQLite databases in data/db
"""
    def __init__(self, database, bot):
        self.database = database
        self.bot = bot

    async def retrieve(self, ctx, category, option):
        """ Retrieve a specific option from a category of options
"""
        # Create query to retrieve data from database
        category, option = category.lower(), option.title()
        query = f"""
        SELECT *
        FROM {category}
        WHERE name=?
        """
        # Try to retrieve data, columns from database
        try:
            content = self.database.read_query(query, option)
            columns = self.database.read_columns()
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        # Zip columns and content into a dictionary
        data = dict(zip(columns, content[0]))
        if not data:
            await ctx.channel.send("No results found.")
        # Construct embed to send data
        embed = discord.Embed(
            title=f"{category.title()}: {option}", color=0xff0000
        )
        # Add each column of data as embed field
        for item in data:
            embed.add_field(name=item.title(), value=data[item])
        # Set footer to command group name
        embed.set_footer(text=ctx.command.full_parent_name)
        # Set embed image corresponding image in data/
        image_name = f"{data['name']}.png"
        image_path = os.path.join(
            "data", ctx.command.full_parent_name.lower(), category, image_name
        )
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        # Send constructed embed
        await ctx.channel.send(file=image, embed=embed)

    async def browse(self, ctx, category):
        """ Allow member to scroll through options for category of map
"""
        # Create query to retrieve data from database
        category = category.lower()
        query = f"""
        SELECT *
        FROM {category}
        """
        # Try to retrieve data, columns from database
        try:
            content = self.database.read_query(query)
            columns = self.database.read_columns()
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        # Create nested dictionary of columns zipped with rows
        data = {
            d["name"]: d for d in [dict(zip(columns, c)) for c in content]
        }
        # Generate a specified embed for member to scroll data with
        embed, image = scrolling_embed(
            ctx.command.full_parent_name, category, data
        )
        # Send generated embed with appropriate reactions
        message = await send_with_reactions(ctx, embed, image)
        # Continuously check for and handle member input
        while True:
            # Handle member reactions
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
            # Break loop when member times out
            except asyncio.TimeoutError:
                break
        # Clear all reactions from and delete message
        await message.clear_reactions()
        await message.delete()

    async def listopts(self, ctx, category):
        """ List all options for a category of map
"""
        # Create query to retrieve data from database
        category = category.lower()
        query = f"""
        SELECT *
        FROM {category}
        """
        # Try to retrieve data from database
        try:
            content = self.database.read_query(query)
        except sqlite3.OperationalError:
            await ctx.channel.send(f"`{category}` is not valid.")
            return
        # Construct embed to send data
        embed = discord.Embed(
            title=category.title(), color=0xff0000,
            description='\n'.join([f"-{r[0]}" for r in content])
        )
        # Set embed footer to command group name
        embed.set_footer(text=ctx.command.full_parent_name)
        # Send constructed embed
        await ctx.channel.send(embed=embed)

    async def retrieve_from_search(self, payload, data):
        """ Retrieve data for current option of embed
"""
        # Process information in payload
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        # Create regular expressions to parse embed
        footer_regex = re.compile(
            r"(Airship|MIRAHQ|Polus|TheSkeld)",
            re.IGNORECASE
        )
        title_regex = re.compile(r"^(.*): (.*)")
        # Get name of map from embed footer
        mapname = footer_regex.search(embed.footer.text).group(1)
        # Get category and option from embed title
        category = title_regex.search(embed.title).group(1)
        option = title_regex.search(embed.title).group(2)
        # Construct embed to send data
        embed = discord.Embed(
            title=f"{category}: {option}", color=0xff0000
        )
        # Add each column of data as embed field
        for item in data[option]:
            embed.add_field(
                name=item.title(), value=data[option][item]
            )
        # Set footer to name of map (command group name)
        embed.set_footer(text=mapname)
        # Set image to the corresponding image in data/
        image_name = f"{option}.png"
        image_path = os.path.join(
            'data', mapname.lower(), category.lower(), image_name
        )
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        # Send constructed embed
        await channel.send(file=image, embed=embed)
        # Delete original message
        await message.delete()

    async def scroll(self, payload, data):
        """ Scroll embed from search command based on the emoji used
"""
        # Process information in payload
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        # Create regular expressions to parse embed
        footer_regex = re.compile(
            r"(Airship|MIRAHQ|Polus|TheSkeld)",
            re.IGNORECASE
        )
        title_regex = re.compile(
            r"^(.*): (.*)"
        )
        # Get name of map from embed footer
        mapname = footer_regex.search(embed.footer.text).group(1)
        # Get category and option from title
        category = title_regex.search(embed.title).group(1)
        option = title_regex.search(embed.title).group(2)
        # Get current index
        index = list(data).index(option)
        # Get new index based on emoji used
        scroll = {
            u'\u23ee': 0, u'\u23ea': index - 5, u'\u25c0': index - 1,
            u'\u25b6': index + 1, u'\u23e9': index + 5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name) % len(data)
        # Re-generate embed with new data
        embed = scrolling_embed(
            mapname, category, data, index=index
        )[0]
        # Edit original message with new embed
        await message.edit(embed=embed)
        await message.remove_reaction(payload.emoji, payload.member)

    async def delete_search(self, payload):
        """ Delete embed from search command
"""
        # Process information in payload
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # Delete message
        await message.delete()


def scrolling_embed(mapname, category, data, *, index=0):
    """ Creates an embed to allow member to browser data with
"""
    # Get current option data
    option_data = list(data.values())[index]
    # Construct embed to send data
    embed = discord.Embed(
        title=f"{category.title()}: {option_data['name']}",
        color=0xff0000
    )
    # Set embed footer to name of map and current page
    embed.set_footer(
        text=f"{mapname}: Page {index+1}/{len(data)}"
    )
    # Add each column of data as embed field
    for item in option_data:
        embed.add_field(
            name=item.title(),
            value=option_data[item]
        )
    # Set embed image to map logo
    image_name = f"{mapname.lower()}.png"
    image_path = os.path.join('data', image_name)
    image = discord.File(image_path, image_name)
    embed.set_image(url=f"attachment://{image_name}")
    # Return constructed embed and image
    return embed, image


async def send_with_reactions(ctx, embed, image):
    """ Sends message with reactions for member to browse data with
"""
    # Send embed and image
    message = await ctx.channel.send(
        embed=embed, file=image
    )
    # Add scroll control reactions
    reactions = [
        u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
        u'\u2714', u'\u274c'
    ]
    for rxn in reactions:
        await message.add_reaction(rxn)
    # Return message for future reference
    return message


def setup(bot):
    """ Adds MapDatabase cog
"""
    bot.add_cog(MapDatabase(bot))
