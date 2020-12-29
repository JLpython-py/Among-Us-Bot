#! python3
# bots.py

import asyncio
import csv
import json
import logging
import re
import os

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

class ParseData:
    def __init__(self, data, name, directory):
        self.data = data
        self.name = name
        self.dir = directory
        self.searches = {
            "actions": {}, "locations": {}, "maps": {}, "tasks": {},
            "vents": {}}

    async def retrieve(self, ctx, category, option):
        data = self.data[category].get(option)
        embed = discord.Embed(
            title=f"{category.title()}: {option.title()}",
            color=0x0000ff)
        for item in data:
            embed.add_field(name=item, value=data[item])
        embed.set_footer(text=self.name)
        image_name = f"{data['Name']}.png"
        image_path = os.path.join(
            'data', self.dir, category, image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)
        await ctx.message.delete()

    async def search(self, ctx, category):
        items = self.data.get(category)
        if ctx.message.author.id in self.searches[category]:
            embed = self.searches[category][ctx.message.author.id]
            await embed.message.delete()
            del self.searches[category][ctx.message.author.id]
        embed = ScrollingEmbed(
            self.dir, ctx.message, self.data, category, self.name)
        embed.manage_embed()
        await embed.send_with_reactions()
        self.searches[category][ctx.message.author.id] = embed
        await ctx.message.delete()

    async def retrieve_from_search(self, payload, category):
        embed = self.searches[category].get(payload.member.id)
        items = self.data.get(category)
        data = items.get(embed.option)
        await self.retrieve(
            embed, embed.category, embed.option)
        del self.searches[category][payload.member.id]

    async def scroll(self, payload, category):
        embed = self.searches[category].get(payload.member.id)
        await embed.scroll(payload)

    async def delete_search(self, payload, category):
        embed = self.searches[category].get(payload.member.id)
        await embed.message.delete()
        del self.searches[category][payload.member.id]

class Airship(commands.Cog):

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.name = "Airship"
        self.dir = 'airship'
        self.data_parser = ParseData(self.data, self.name, self.dir)

class MiraHQ(commands.Cog):

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.name = "MIRA HQ"
        self.dir = 'mirahq'
        self.data_parser = ParseData(self.data, self.name, self.dir)

class Polus(commands.Cog):

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.name = "Polus"
        self.dir = 'polus'
        self.data_parser = ParseData(self.data, self.name, self.dir)

class TheSkeld(commands.Cog):

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.name = "The Skeld"
        self.dir = 'theskeld'
        self.data_parser = ParseData(
            self.data, self.name, self.dir)

class MapBot(commands.Bot):
    def __init__(self, *, prefix, name):
        '''
'''
        commands.Bot.__init__(
            self, command_prefix=prefix,
            case_insensitive=True, self_bot=False)
        self.read_files()
        self.name = name
        self.add_cog(MiraHQ(self, self.data['mirahq']))
        self.add_cog(Polus(self, self.data['polus']))
        self.add_cog(TheSkeld(self, self.data['theskeld']))
        self.map_cogs = {
            'mirahq': self.get_cog('MiraHQ'),
            'polus': self.get_cog('Polus'),
            'theskeld': self.get_cog('TheSkeld')}
        self.execute_commands()

    def read_files(self):
        ''' Read CSV data for each map
'''
        self.data = {}
        for maps in ['airship', 'mirahq', 'polus', 'theskeld']:
            map_data = {}
            directory = os.path.join('data', maps)
            directories = [d for d in os.listdir(directory)\
                           if os.path.isdir(os.path.join(directory, d))]
            for direct in directories:
                csvfile = os.path.join(
                    directory, direct, f"{direct}.csv")
                with open(csvfile) as file:
                    data = list(csv.reader(file))
                    headings = data.pop(0)
                map_data[direct] = {}
                for row in data:
                    info = dict(zip(headings, row))
                    map_data[direct].setdefault(info['Name'], info)
            self.data.setdefault(maps, map_data)

    async def on_ready(self):
        ''' Notify developer that a MapBot-class bot is active
'''
        logging.info("Ready: %s", self.name)

    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        name = payload.emoji.name
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        footer_regex = re.compile(r'(.*): Page [0-9]+/[0-9]+')
        title_regex = re.compile(r'(.*): .*')
        mapcog = footer_regex.search(embed.footer.text).group(1).lower()
        cog = self.map_cogs.get(''.join(mapcog.split()))
        category = title_regex.search(embed.title).group(1).lower()
        if name in [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9',
            u'\u23ed']:
            await cog.data_parser.scroll(payload, category)
        elif name == u'\u2714':
            await cog.data_parser.retrieve_from_search(payload, category)
        elif name == u'\u274c':
            await cog.data_parser.delete_search(payload, category)

    def execute_commands(self):
        @self.command(name="retrieve", pass_context=True,
                      aliases=["r"])
        async def retrieve(ctx, mapname, category, option):
            ''' [Embed] Returns data about the given option on the map
                <mapname>: MiraHQ, TheSkeld, Polus
                <category>: actions, locations, tasks, maps, vents
                <option>: *Varies with the <category> command
'''
            mapname = mapname.lower()
            cog = self.map_cogs.get(mapname)
            if cog is None:
                await ctx.send(
                    f"`{mapname}` is not an active Among Us map")
                return
            if self.data[mapname].get(category) is None:
                await ctx.send(
                    f"`category={category}` is not valid")
                return
            if self.data[mapname][category].get(option) is None:
                await ctx.send(
                    f"`option={option}` is not valid")
                return
            await cog.data_parser.retrieve(ctx, category, option)

        @self.command(name="search", pass_context=True,
                      aliases=["s"])
        async def search(ctx, mapname, category):
            ''' [Embed] Used to browse through the options for a category
                Use the button reactions to scroll through the options
                Use the check reaction to select the option
                Use the 'x' reaction to close the message
                <mapname>: MiraHQ, TheSkeld, Polus
                <category>: actions, locations, tasks, maps, vents
'''
            mapname = mapname.lower()
            cog = self.map_cogs.get(mapname)
            if cog is None:
                await ctx.send(
                    f"`{mapname}` is not an active Among Us map")
                return
            if self.data[mapname].get(category) is None:
                await ctx.send(
                    f"`category={category}` is not valid")
                return
            await cog.data_parser.search(ctx, category)

class ScrollingEmbed:
    def __init__(self, directory, message, data, category, name):
        self.dir = directory
        self.channel = message.channel
        self.memberid = message.author.id
        self.category = category
        self.items = data.get(self.category)
        self.name = name

    def manage_embed(self, index=0):
        self.option = list(self.items)[index]
        self.data = self.items.get(self.option)
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        self.embed.set_footer(
            text=f"{self.name}: Page {index+1}/{len(self.items)}")
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        image_name = f"{self.dir}.png"
        image_path = os.path.join('data', image_name)
        self.image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")

    async def send_with_reactions(self):
        self.message = await self.channel.send(
            file=self.image, embed=self.embed)
        reactions = [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
            u'\u2714', u'\u274c']
        for rxn in reactions:
            await self.message.add_reaction(rxn)

    async def scroll(self, payload):
        if payload.member.id != self.memberid:
            await self.message.remove_reaction(
                payload.emoji, payload.member)
            return
        index = list(self.items).index(self.option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index-5, u'\u25c0': index-1,
            u'\u25b6': index+1, u'\u23e9': index+5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name)%len(self.items)
        self.manage_embed(index=index)
        await self.message.edit(embed=self.embed)
        await self.message.remove_reaction(payload.emoji, payload.member)

def main():
    token = os.environ.get("token", None)
    if token is None:
        with open(os.path.join('data', 'token.txt')) as file:
            token = file.read()
    assert token is not None
    loop = asyncio.get_event_loop()
    discord_bot = MapBot(
        prefix="+", name="AmongUs MapBot")
    loop.create_task(discord_bot.start(token))
    loop.run_forever()

if __name__ == '__main__':
    main()
