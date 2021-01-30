#! python3
# mapdatabase.py

import os
import re

import discord
from discord.ext import commands


class MapDatabase(commands.Cog):
    """ Allow member to explore available information in Among Us
"""
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.searches = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """ Manage response to added reaction
"""
        if payload.member.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        if payload.member.id == message.author.id:
            return
        if not any([m in embed.footer.text for m in [
            "Airship", "MIRAHQ", "Polus", "TheSkeld"
        ]]):
            return
        if payload.emoji.name in [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed'
        ]:
            await self.scroll(payload)
        elif payload.emoji.name == u'\u2714':
            await self.retrieve_from_search(payload)
        elif payload.emoji.name == u'\u274c':
            await self.delete_search(payload)

    @commands.group(name="MIRAHQ", case_insensitive=True, pass_context=True,
                    aliases=["MIRA", "MH"])
    async def mira_hq(self, ctx):
        """ Command group to parse information from MIRA HQ data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid MIRA HQ command passed")

    @mira_hq.group(name="retrieve", pass_context=True, aliases=["r"])
    async def mirahq_retrieve(self, ctx, category, option):
        """ Retrieve option for category in MIRA HQ data
"""
        await self.retrieve(ctx, category, option)

    @mira_hq.group(name="search", pass_context=True, aliases=["s"])
    async def mirahq_search(self, ctx, category):
        """ Search options for category in MIRA HQ data
"""
        await self.search(ctx, category)

    @mira_hq.group(name="listopts", pass_context=True, aliases=["ls"])
    async def mirahq_listopts(self, ctx, category):
        """ List options for category in MIRA HQ data
"""
        await self.listopts(ctx, category)

    @commands.group(name="Polus", case_insensitive=True, pass_context=True,
                    aliases=["P"])
    async def polus(self, ctx):
        """ Command group to parse information from Polus data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Polus command passed")

    @polus.group(name="retrieve", pass_context=True, aliases=["r"])
    async def polus_retrieve(self, ctx, category, option):
        """ Retrieve option for category in Polus data
"""
        await self.retrieve(ctx, category, option)

    @polus.group(name="search", pass_context=True, aliases=["s"])
    async def polus_search(self, ctx, category):
        """ Search options for category in Polus data
"""
        await self.search(ctx, category)

    @polus.group(name="listopts", pass_context=True, aliases=["ls"])
    async def polus_listopts(self, ctx, category):
        """ List options for category in Polus data
"""
        await self.listopts(ctx, category)

    @commands.group(name="TheSkeld", case_insensitive=True, pass_context=True,
                    aliases=["Skeld", "TS"])
    async def the_skeld(self, ctx):
        """ Command group to parse information from The Skeld data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid The Skeld command passed")

    @the_skeld.group(name="retrieve", pass_context=True, aliases=["r"])
    async def theskeld_retrieve(self, ctx, category, option):
        """ Retrieve option for category in The Skeld data
"""
        await self.retrieve(ctx, category, option)

    @the_skeld.group(name="search", pass_context=True, aliases=["s"])
    async def theskeld_search(self, ctx, category):
        """ Search options for category in The Skeld data
"""
        await self.search(ctx, category)

    @the_skeld.group(name="listopts", pass_context=True, aliases=["ls"])
    async def theskeld_listopts(self, ctx, category):
        """ List options for category in The Skeld data
"""
        await self.listopts(ctx, category)

    async def retrieve(self, ctx, category, option):
        """ Retrieve data for option for category of map
"""
        # Validate category and option
        category, option = category.lower(), option.title()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        if option not in self.data[mapname][category]:
            await ctx.send(f"`option={option}` is not valid")
            return
        # Get data from category and option and send in embed
        data = self.data[mapname][category][option]
        embed = discord.Embed(
            title=f"{category.title()}: {option}",
            color=0x0000ff)
        for item in data:
            embed.add_field(name=item, value=data[item])
        embed.set_footer(text=ctx.command.full_parent_name)
        image_name = f"{data['Name']}.png"
        image_path = os.path.join(
            'data', mapname, category, image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)

    async def search(self, ctx, category):
        """ Allow member to scroll through options for category of map
"""
        # Validate category
        category = category.lower()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        # Delete any existing search
        if ctx.author.id in self.searches:
            embed = self.searches[ctx.author.id]
            await embed.message.delete()
            del self.searches[ctx.author.id]
        # Create embed for member to scroll data with
        embed = ScrollingEmbed(
            ctx.command.full_parent_name, category, self.data)
        embed.manage_embed()
        await embed.send_with_reactions(ctx.message)
        self.searches.setdefault(ctx.author.id, embed)

    async def listopts(self, ctx, category):
        """ List all options for a category of map
"""
        # Validate category
        category = category.lower()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        # Get data for category and send all options in embed
        data = self.data[mapname][category]
        embed = discord.Embed(
            title=category.title(), color=0xff0000)
        for item in data:
            text = '\n'.join([
                f"`{k}`: {v[:20]}..." for k, v in data[item].items()])
            embed.add_field(name=item, value=text)
        embed.set_footer(text=ctx.command.full_parent_name)
        image_name = f"{mapname}.png"
        image_path = os.path.join('data', image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)

    async def retrieve_from_search(self, payload):
        """ Retrieve data for current option of embed
"""
        # Process payload information
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # Get map and category from embed
        footer_regex = re.compile(
            fr"^({'|'.join([c.name for c in self.get_commands()])}):")
        mapname = footer_regex.search(
            message.embeds[0].footer.text).group(1)
        title_regex = re.compile(
            r"^(.*):")
        category = title_regex.search(
            message.embeds[0].title).group(1).lower()
        # Get data from embed from searches by payload
        option = self.searches.get(payload.member.id).option
        data = self.data[mapname.lower()][category][option]
        # Edit embed to mimic retrieve command
        embed = discord.Embed(
            title=f"{category.title()}: {option.title()}",
            color=0x0000ff)
        for item in data:
            embed.add_field(name=item, value=data[item])
        embed.set_footer(text=mapname)
        image_name = f"{data['Name']}.png"
        image_path = os.path.join(
            'data', mapname.lower(), category, image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await channel.send(file=image, embed=embed)
        await message.delete()
        del self.searches[payload.member.id]

    async def scroll(self, payload):
        """ Scroll embed from search command based on the emoji used
"""
        embed = self.searches.get(payload.member.id)
        await embed.scroll(payload)

    async def delete_search(self, payload):
        """ Delete embed from search command
"""
        embed = self.searches.get(payload.member.id)
        await embed.message.delete()
        del self.searches[payload.member.id]


class ScrollingEmbed:
    """ Generate embed which a member can scroll by using reactions
"""
    def __init__(self, name, category, data):
        self.name = name
        self.category = category
        self.items = data[self.name.lower()][self.category]
        self.option = list(self.items)[0]
        self.data = self.items.get(self.option)

        self.embed = None
        self.image = None
        self.message = None
        self.memberid = 0

    def manage_embed(self, index=0):
        """ Edit the existing embed with new data
"""
        # Create embed with data in body and page number in footer
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        self.embed.set_footer(
            text=f"{self.name}: Page {index+1}/{len(self.items)}")
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        # Attach image to embed
        image_name = f"{self.name.lower()}.png"
        image_path = os.path.join('data', image_name)
        self.image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")

    async def send_with_reactions(self, message):
        """ Send generated embed and react with designated emojis
"""
        self.memberid = message.author.id
        self.message = await message.channel.send(
            file=self.image, embed=self.embed)
        reactions = [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
            u'\u2714', u'\u274c']
        for rxn in reactions:
            await self.message.add_reaction(rxn)

    async def scroll(self, payload):
        """ Get new data based on emoji used
"""
        # Validate member who reacted requested embed
        if payload.member.id != self.memberid:
            await self.message.remove_reaction(
                payload.emoji, payload.member)
            return
        # Get current index and scroll according to emoji
        index = list(self.items).index(self.option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index-5, u'\u25c0': index-1,
            u'\u25b6': index+1, u'\u23e9': index+5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name) % len(self.items)
        # Get new option and new data from new index
        self.option = list(self.items)[index]
        self.data = self.items.get(self.option)
        self.manage_embed(index=index)
        await self.message.edit(embed=self.embed)
        await self.message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
    """ Allow lib.bot.__init__.py to add MapDatabase cog
"""
    bot.add_cog(MapDatabase(bot))
